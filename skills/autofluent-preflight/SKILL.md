---
name: autofluent-preflight
description: Check Fluent case readiness, mesh quality, units, materials, boundaries and wall treatment before solving. 用于 Fluent 算例预检查和设置一致性检查。
---

# 算例预检查

## Runtime

Requires AutoFluent MCP 0.3.0 (36 tools), Fluent 2023 R1 and PyFluent 0.37.0 for solver operations. Call fluent_diagnostics and fluent_sessions first when a solver is needed. Reuse an idle, appropriate session; use the installed autofluent-gui skill only when a visible window is requested. If the new tool is missing, reconnect the upgraded MCP; do not claim it ran.

Poll every returned job_id with fluent_job_status until terminal. A succeeded job does not prove convergence or applicability. Use new workspace-relative output directories. Preserve unsaved case changes before loading another case or initializing. Never print or publish server-info credentials. Read references/example.json for the argument structure, replacing model-specific values from the actual case.

## Workflow

Call fluent_preflight with session_id, directory and spec. Inspect real boundary names and material definitions first. Supply expected_energy/expected_steady and expected_materials only for the intended physics. expected_materials maps fluid material names to native constant-property names/values, e.g. density, viscosity, thermal_conductivity, specific_heat. expected_length_m and axial_direction compare native metre extents to engineering dimensions.

The result saves models, material/boundary/zone settings and native mesh-check/quality output. It checks positive minimum cell volume, minimum orthogonal quality against a configurable threshold (default 0.1), and expected axial length when available. These thresholds are screening criteria, not universal mesh-quality approval. Review aspect ratio with flow alignment and cell shape.

Inspect boundary types/values, source terms and turbulence/wall-treatment settings in snapshot. Use fluent_compute_reports for y-plus on an already solved case; an unsolved field does not establish wall-resolution suitability. Show pass/fail/unknown/review_required separately. ready=null means outstanding review, not ready. Do not auto-rescale, change material or select a turbulence model without the requested physical basis.
