---
name: autofluent-grid-study
description: Run and compare coarse medium fine Fluent cases and calculate eligible Richardson extrapolation and GCI. 用于三套网格的网格收敛分析。
---

# 网格无关性验证

## Runtime

Requires AutoFluent MCP 0.3.0 (36 tools), Fluent 2023 R1 and PyFluent 0.37.0 for solver operations. Call fluent_diagnostics and fluent_sessions first when a solver is needed. Reuse an idle, appropriate session; use the installed autofluent-gui skill only when a visible window is requested. If the new tool is missing, reconnect the upgraded MCP; do not claim it ran.

Poll every returned job_id with fluent_job_status until terminal. A succeeded job does not prove convergence or applicability. Use new workspace-relative output directories. Preserve unsaved case changes before loading another case or initializing. Never print or publish server-info credentials. Read references/example.json for the argument structure, replacing model-specific values from the actual case.

## Workflow

Obtain three distinct existing coarse/medium/fine case files with matching geometry, physics, boundary conditions and schemes. Never duplicate one mesh and label it three levels. Ask for missing meshes if they are not available; do not report grid independence from a single grid.

For a heated-pipe batch, run fluent_run_pipe_study for each mesh in its own directory with identical pipe/criteria and requested velocity, export=false when only comparison is needed. Poll and require each case status=complete. Load each saved solution using fluent_read_file, compute pressure performance using fluent_pressure_performance with identical sampling definitions, and collect Nu and dp. Preserve source result paths in a local provenance file.

Compute representative h=(domain volume/cell count)^(1/dimension) or use documented systematic mesh spacing; do not use cell count directly as spacing. Provide levels [{label,spacing,values:{Nu,dp},converged}], comparable and safety_factor to fluent_grid_convergence. Keys must match across levels; the tool sorts fine to coarse. It supports equal refinement ratios within 1%, each >1.1, monotonic convergent sequences, and Fs>=1.25. Unequal ratios, oscillation, identical values, zero references or unconverged cases receive reasons and no GCI. It does not silently substitute theoretical order.

Deliver all grid values, relative changes, observed p, extrapolated values, fine/medium GCI and asymptotic ratio when valid. Check asymptotic ratio near one alongside actual refinement design. GCI is discretization uncertainty, not physical-model validation. Source: https://www.grc.nasa.gov/www/wind/valid/tutorial/spatconv.html
