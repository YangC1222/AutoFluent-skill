# Setup and recovery

## Requirements

- Licensed local Ansys Fluent 2023 R1, interactive desktop access.
- Python 3.10–3.13 with `ansys-fluent-core==0.37.0`; use the existing AutoFluent environment.
- The [AutoFluent MCP](https://github.com/YangC1222/AutoFluent-) configured as `autofluent` in Codex.
- `AWP_ROOT231` pointing to the actual v231 installation. If it is set only in the MCP configuration, pass that same value to the launcher's process environment.

The skill does not install Fluent, provide a license, expose HTTP ports, or configure the MCP automatically. `agents/openai.yaml` declares the MCP dependency; that declaration is not installation.

## Install skill

Clone this repository and copy its `SKILL.md`, `agents`, `scripts`, and `references` into `$CODEX_HOME/skills/autofluent-gui` (normally `~/.codex/skills/autofluent-gui`). Do not copy `.git`, runtime data or credentials. If an existing skill is present, inspect it before replacing files. Start a new Codex chat or reload skill discovery if it is not immediately available.

Invoke `$autofluent-gui` and request a visible Fluent window. Resolve the helper relative to the installed skill directory, not a developer-specific path.

## Connect a GUI opened manually

In Fluent solver mode, use **File → Applications → Server → Start** to save a server-info file inside the MCP workspace. Then use `fluent_connect` and poll its job. The file contains credentials; do not display its contents. Source: [PyFluent launch/connect guide](https://fluent.docs.pyansys.com/version/stable/user_guide/session/launching_ansys_fluent.html).

## Failure and recovery

- Missing license or startup timeout: inspect the local launch log and any Fluent dialogs. Check for an existing GUI before starting another process. Do not auto-retry indefinitely.
- `gui_visible=false`: GUI mode was requested but a visible window was not confirmed. Check the interactive Windows desktop and startup dialogs. Do not claim live GUI verification.
- MCP capacity reached: identify existing sessions and unsaved work. Disconnect an unused borrowed session only when authorized; do not terminate another simulation.
- Stale server-info: the associated Fluent process may have closed. Do not overwrite an old credential file; start a new run directory or reconnect to a live GUI.
- Read-only GUI viewing can coexist with calculation. Parameter editing, initialization and case loading must be coordinated with MCP jobs.
- For screenshots or native contour display, use available scoped capture/render capabilities. AutoFluent 0.2 adds native PNG export through fluent_render_contour. Reconnect MCP after upgrading and verify 28 tools. There is no video streaming tool. Do not advertise an embedded live viewer.
