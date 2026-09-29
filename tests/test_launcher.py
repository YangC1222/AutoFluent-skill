import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location('launcher', Path(__file__).parents[1] / 'scripts' / 'launch_gui.py')
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class LauncherTests(unittest.TestCase):
    def test_gui_persists_and_credentials_stay_out_of_status(self):
        api = Mock()
        api.get_fluent_version.return_value = '23.1.0'
        api.connection_properties = SimpleNamespace(ip='127.0.0.1', port=12345,
            password='test-secret-not-for-output', cortex_pid=4321)
        backend = SimpleNamespace(launch_fluent=Mock(return_value=api))
        with tempfile.TemporaryDirectory() as tmp, patch.object(launcher, 'visible_windows', return_value=1):
            result = launcher.launch(tmp, backend=backend)
            self.assertTrue(result['gui_visible'])
            self.assertNotIn('test-secret', json.dumps(result))
            info = Path(tmp) / result['server_info_file']
            self.assertEqual(info.read_text().splitlines(), ['127.0.0.1:12345', 'test-secret-not-for-output'])
            self.assertNotIn('test-secret', (info.parent / 'status.json').read_text())
            options = backend.launch_fluent.call_args.kwargs
            self.assertEqual(options['ui_mode'], 'gui')
            self.assertEqual(options['product_version'], '23.1.0')
            self.assertFalse(options['cleanup_on_exit'])
            self.assertFalse(options['start_watchdog'])
            api.exit.assert_called_once_with(timeout=10, timeout_force=False)

    def test_never_overwrites_existing_connection(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'server-info.txt'
            file.write_text('existing')
            with self.assertRaises(FileExistsError):
                launcher.save_connection(file, SimpleNamespace(ip='127.0.0.1',port=123,password='test'))
            self.assertEqual(file.read_text(), 'existing')

    def test_rejects_invalid_processors_before_launch(self):
        backend = Mock()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                launcher.launch(tmp, processors=0, backend=backend)
        backend.launch_fluent.assert_not_called()

    def test_version_mismatch_terminates_only_new_empty_session(self):
        api = Mock()
        api.get_fluent_version.return_value = '24.2.0'
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                launcher.launch(tmp, backend=SimpleNamespace(launch_fluent=Mock(return_value=api)))
            self.assertEqual(list(Path(tmp).rglob('server-info.txt')), [])
        api.exit.assert_called_once_with(timeout=10, timeout_force=True)


if __name__ == '__main__':
    unittest.main()
