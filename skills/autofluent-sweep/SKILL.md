---
name: autofluent-sweep
description: Run resumable Cartesian scans of Fluent numeric boundary conditions and constant material properties. 用于速度热流入口温度物性多参数扫描。
---

# 多参数扫描

## Runtime

Requires AutoFluent MCP 0.3.0 (36 tools), Fluent 2023 R1 and PyFluent 0.37.0 for solver operations. Call fluent_diagnostics and fluent_sessions first when a solver is needed. Reuse an idle, appropriate session; use the installed autofluent-gui skill only when a visible window is requested. If the new tool is missing, reconnect the upgraded MCP; do not claim it ran.

Poll every returned job_id with fluent_job_status until terminal. A succeeded job does not prove convergence or applicability. Use new workspace-relative output directories. Preserve unsaved case changes before loading another case or initializing. Never print or publish server-info credentials. Read references/example.json for the argument structure, replacing model-specific values from the actual case.

## Workflow

Inspect target settings with fluent_inspect_settings/fluent_get_settings before constructing axes. Call fluent_parameter_sweep with session_id, directory and spec containing base_case, axes, pipe, criteria and resume. Each axis has unique name, public numeric scalar path under setup/boundary_conditions or setup/materials, and finite distinct values. At most four axes and 100 total Cartesian combinations are allowed.

Axes can include inlet velocity, inlet temperature, wall heat flux and constant material values. Material axes must set pipe_property to density/viscosity/conductivity/specific_heat so convergence energy/Re/Pr calculations match the changed property. This solver workflow is for a constant-property, steady, heated single-inlet/outlet pipe; pressure outlets and arbitrary multiphysics are not a generic optimization capability.

The tool reloads the base and hybrid-initializes each combination. Save unsaved work before starting. It records parameter values, histories, status and case/data checksums. Repeating an identical specification resumes by skipping verified complete cases; changed axes/base/settings need a new directory. Interrupted/unconverged cases use new attempts. Inspect per-case status, not just job success. Cancellation happens between chunks.

Geometry scans require separately remeshed input cases and an outer loop over those cases; do not mutate geometric dimensions in a fixed mesh. Do not claim checkpoints resume iterations: recovery is at case level. A retained .study.lock after a crash must be verified stale before removal.
