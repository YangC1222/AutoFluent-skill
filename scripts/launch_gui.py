"""Launch a persistent visible Fluent 23.1 GUI for an existing AutoFluent MCP."""
from __future__ import annotations

import argparse
import contextlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time
import traceback
import uuid


def visible_windows(pid):
    """Return visible top-level window count for one known Fluent process."""
    if sys.platform != 'win32' or not pid:
        return None
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    count = 0
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    @callback_type
    def visit(hwnd, _):
        nonlocal count
        owner = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if owner.value == int(pid) and user32.IsWindowVisible(hwnd):
            count += 1
        return True

    user32.EnumWindows(visit, 0)
    return count


def check_environment():
    version = importlib.metadata.version('ansys-fluent-core')
    if version != '0.37.0':
        raise RuntimeError(f'Requires ansys-fluent-core==0.37.0; found {version}.')
    root = os.environ.get('AWP_ROOT231')
    if not root:
        raise RuntimeError('Set AWP_ROOT231 to the Fluent 2023 R1 installation root.')
    binary = Path(root) / ('fluent/ntbin/win64/fluent.exe' if os.name == 'nt' else 'fluent/bin/fluent')
    if not binary.is_file():
        raise RuntimeError('Fluent 2023 R1 executable was not found beneath AWP_ROOT231.')
    return {'pyfluent_version': version, 'fluent_version': '23.1.0', 'executable_found': True}


def save_connection(path, props):
    # Match PyFluent's two-line server-info format without logging the password.
    if not props.ip or not props.port or not props.password:
        raise RuntimeError('Incomplete Fluent connection information.')
    if any('\n' in str(v) or '\r' in str(v) for v in (props.ip, props.port, props.password)):
        raise RuntimeError('Invalid connection information.')
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(f'{props.ip}:{props.port}\n{props.password}\n')


def launch(workspace, processors=2, mode='solver', backend=None):
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError('Workspace must be an existing directory.')
    if processors < 1:
        raise ValueError('Processors must be positive.')
    if mode not in ('solver', 'meshing'):
        raise ValueError('Mode must be solver or meshing.')
    run = workspace / '.autofluent-gui' / uuid.uuid4().hex
    run.mkdir(parents=True, mode=0o700)
    info = run / 'server-info.txt'
    api = None
    with (run / 'launcher.log').open('w', encoding='utf-8') as log:
        try:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                if backend is None:
                    import ansys.fluent.core as backend
                api = backend.launch_fluent(product_version='23.1.0', mode=mode,
                    dimension=3, precision='double', processor_count=processors,
                    ui_mode='gui', cleanup_on_exit=False, start_watchdog=False,
                    start_transcript=False, start_timeout=180, cwd=str(run))
                version = api.get_fluent_version()
                actual = str(getattr(version, 'value', version))
                if actual not in ('23.1', '23.1.0'):
                    # This process was created here and has not loaded user work.
                    api.exit(timeout=10, timeout_force=True)
                    raise RuntimeError('Launched Fluent version does not match 23.1.')
                props = api.connection_properties
                save_connection(info, props)
                count = visible_windows(props.cortex_pid)
                deadline = time.monotonic() + 10
                while count == 0 and time.monotonic() < deadline:
                    time.sleep(.5)
                    count = visible_windows(props.cortex_pid)
                result = {'status':'ready', 'mode':mode, 'version':actual,
                    'server_info_file':info.relative_to(workspace).as_posix(),
                    'gui_requested':True, 'gui_visible':None if count is None else count > 0,
                    'visible_window_count':count, 'cortex_pid':props.cortex_pid,
                    'lifecycle':'GUI stays open; MCP close disconnects only'}
                # cleanup_on_exit=False makes this disconnect, not solver termination.
                api.exit(timeout=10, timeout_force=False)
            (run / 'status.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
            return result
        except Exception as exc:
            traceback.print_exc(file=log)
            # Do not expose connection properties or arbitrary exception messages.
            raise RuntimeError(f'GUI startup did not complete ({type(exc).__name__}); inspect {run / "launcher.log"}. A GUI may remain open; check before retrying.') from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True, type=Path)
    parser.add_argument('--processors', type=int, default=2)
    parser.add_argument('--mode', choices=['solver','meshing'], default='solver')
    parser.add_argument('--check', action='store_true', help='Check prerequisites without consuming a license')
    args = parser.parse_args()
    try:
        env = check_environment()
        result = env if args.check else launch(args.workspace, args.processors, args.mode)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'status':'failed','error':str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
