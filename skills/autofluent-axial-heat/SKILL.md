---
name: autofluent-axial-heat
description: Compute and plot local axial wall/bulk temperatures, heat flux, h and Nu from Fluent cross sections and wall bands. 用于沿程局部换热分析。
---

# 轴向局部换热

## Runtime

Requires AutoFluent MCP 0.3.0 (36 tools), Fluent 2023 R1 and PyFluent 0.37.0 for solver operations. Call fluent_diagnostics and fluent_sessions first when a solver is needed. Reuse an idle, appropriate session; use the installed autofluent-gui skill only when a visible window is requested. If the new tool is missing, reconnect the upgraded MCP; do not claim it ran.

Poll every returned job_id with fluent_job_status until terminal. A succeeded job does not prove convergence or applicability. Use new workspace-relative output directories. Preserve unsaved case changes before loading another case or initializing. Never print or publish server-info credentials. Read references/example.json for the argument structure, replacing model-specific values from the actual case.

## Workflow

Use a saved converged case/data without reinitialization. Identify the flow axis, coordinates in metres, fluid-side heated wall and conductivity. Call fluent_axial_heat_transfer. Automatic mode accepts positions, axis, wall and half_width; it creates coordinate planes and clips narrow wall bands using a fixed 23.1 command. Existing-surface mode instead accepts stations [{x,bulk_surface,wall_surface}]. Choose exactly one mode.

Automatic planes cut the whole domain: use existing fluid-only cross sections for multiple passages, recirculation or ambiguous intersected zones. Confirm wall-band extents stay inside the heated section and the band width resolves axial variations. The tool retains generated named surfaces for inspection.

Tw uses Wall Temperature, not Static Temperature on clipped surfaces. Tb uses mass-averaged fluid temperature. q uses the heat-flux field and explicit heat_into_fluid_sign (1 or -1); check the sign against the original wall heat-transfer report, never infer it from desired h. h=q/(Tw-Tb), Nu=hD/k. Null/invalid rows indicate inconsistent sign, tiny temperature difference or invalid area. Do not replace them with zero.

Deliver CSV/JSON plus PNG/SVG/PDF plots; install MCP reports extra if plot_error reports missing dependencies. Inspect plots and table values. These are wall-band means, not pointwise wall coefficients; variable cp requires enthalpy-based bulk temperature outside this workflow.
