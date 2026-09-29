---
name: autofluent-gui
description: Operate local Ansys Fluent 2023 R1 through AutoFluent MCP with a visible native Fluent window. Use for opening Fluent interactively, importing cases, changing simulation settings, rendering native contours, running resumable pipe velocity studies, checking convergence, and exporting Excel/theory comparisons while the user can inspect the same solver session.
---

# AutoFluent GUI

Use the `autofluent` MCP server for solver operations and this skill's launcher for a visible Fluent 2023 R1 window. The GUI is a separate native desktop window, not an embedded Codex panel or a screenshot stream. Prefer API operations over mouse automation.

## Establish the session

1. Call `fluent_diagnostics` and `fluent_sessions`. Check 23.1 installation, workspace, session limit, active jobs, and available processors. Use the Python environment containing AutoFluent and **ansys-fluent-core==0.37.0**. Do not upgrade PyFluent automatically; newer releases may drop 2023 R1.
2. Reuse a known visible session when available. A session ID alone does not prove GUI visibility. Do not close or replace an existing case to make room without accounting for unsaved work. If the user only wants background computation, the existing `fluent_launch` is sufficient.
3. For a new visible session, run the bundled helper with that Python executable and the exact workspace reported by diagnostics:

   ```text
   python <skill-dir>/scripts/launch_gui.py --workspace <MCP-workspace> --processors 2
   ```

   The helper prints JSON containing a workspace-relative `server_info_file`, mode, and GUI visibility evidence. Launch can take several minutes. Poll the shell process until it finishes. If it fails, read its reported error/log locally; do not launch repeatedly or dump credential files. `--check` checks dependencies without starting Fluent.
4. Call `fluent_connect(server_info_file=<returned path>, mode=<returned mode>)`. Poll `fluent_job_status` until succeeded, then retain its `result.session_id`. If the MCP call is unavailable, report the missing MCP configuration instead of claiming connection succeeded. Read [references/setup.md](references/setup.md) for installation and connection recovery.
5. The helper starts Fluent with `cleanup_on_exit=False` and no watchdog, so the GUI survives launcher exit. The MCP connection is borrowed: `fluent_close` disconnects it but does not terminate the visible application. After saving, the user may close Fluent normally. Never describe disconnect as solver shutdown.

## Operate one shared model

- Ask the user to finish manual edits before automatic mutations if they are actively editing. API jobs and GUI edits affect the same solver. Between tasks, re-read relevant settings; do not assume cached settings survived manual edits.
- Inspect setting names, allowed values, surfaces and boundaries before writing. Preserve case physics and units unless changes are requested. Use workspace-relative paths and new output filenames.
- Loading case/data changes the visible session. Initialization resets the solution. Account for unsaved changes before either action; reusing a saved case does not require initialization for postprocessing.
- Every operation returning `job_id` must complete before another operation on that session. Monitor with `fluent_job_status` and `fluent_logs`. Cancellation takes effect between iteration chunks.
- Job success is not convergence: inspect residual trends, mass/energy balance, and relevant monitored quantities. Report which checks were actually performed.
- The user can rotate/zoom the mesh, inspect settings and use Fluent's native plotting controls. Do not promise that API mutations automatically open or refresh every GUI panel. AutoFluent 0.2 exposes native contour rendering; verify the four workflow tools are available before using them.
- Export requested results through supported tools. Identify plane coordinates, vector component versus magnitude, units, averaging definitions, and any interpolation. Saved images are snapshots, not live interactive views.

## Native plotting and pipe studies

Read [references/workflows.md](references/workflows.md) for native contours, resumable velocity sweeps, combined convergence checks, and nine-column Excel/theory exports. Use these MCP workflows for matching requests. Confirm boundaries, material properties, heating assumptions and dimensions from the actual model. Defaults are examples, not inferred physics. Check the returned convergence flag.

## Credential and output handling

Server-info files contain a local connection password. Keep them in the workspace's `.autofluent-gui/` directory; never print, commit, or paste their contents. Only the path belongs in tool calls or user messages. Public repositories must exclude runtime directories and CFD case/data files.

Report the actual state: GUI requested versus confirmed visible, MCP connection success, current loaded case, and whether a restart/new chat is needed for skill discovery. Do not claim the Fluent GUI is inside Codex.
