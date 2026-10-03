---
name: autofluent-monitor
description: Open a local live AutoFluent dashboard with progress residual and balance trends logs cancellation and result downloads. 用于监控计算和取消运行任务。
---

# 计算监控面板

## Runtime

Requires AutoFluent MCP 0.3.0 (36 tools), Fluent 2023 R1 and PyFluent 0.37.0 for solver operations. Call fluent_diagnostics and fluent_sessions first when a solver is needed. Reuse an idle, appropriate session; use the installed autofluent-gui skill only when a visible window is requested. If the new tool is missing, reconnect the upgraded MCP; do not claim it ran.

Poll every returned job_id with fluent_job_status until terminal. A succeeded job does not prove convergence or applicability. Use new workspace-relative output directories. Preserve unsaved case changes before loading another case or initializing. Never print or publish server-info credentials. Read references/example.json for the argument structure, replacing model-specific values from the actual case.

## Workflow

Call fluent_dashboard(action="start") and open the returned local URL. The page refreshes every two seconds and shows this MCP process's recent jobs, progress, residual/h/mass/energy trends, solver logs and available result downloads. Trends accumulate while the page is open; reload does not reconstruct full history. A disconnected page must be reported as disconnected, not live.

The page binds only 127.0.0.1 and uses a random URL token. Keep its URL local. It can cancel eligible jobs cooperatively after their current chunk; it cannot force-stop native file operations or edit solver physics. Cancel only the user's intended job. fluent_dashboard(action="stop") stops the page server without closing Fluent.

Keep the hosting MCP process running. The dashboard sees only that process's sessions/jobs, not calculations in another MCP or Python process. Use Fluent's native GUI for geometry interaction; this dashboard is not a screen stream. Native results downloads are restricted to generated artifact paths within workspace.
