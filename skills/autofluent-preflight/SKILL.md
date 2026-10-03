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

## Meshing preference — structured first

For every new mesh or remeshing task, first assess structured meshing feasibility from the actual geometry and topology. Prefer mapped quadrilateral meshes in 2D and mapped/swept or multiblock hexahedral meshes in 3D when feasible. Consider reasonable partitioning, sweep source/target compatibility and pipe O-grid/block layouts before abandoning the structured route. Verify mesh quality and near-wall resolution; do not force a poor structured mesh merely to satisfy the preference.

Use another method only after identifying why the structured approach is unsuitable or unavailable. State the specific geometric/topological, quality or tooling limitation, then select a suitable alternative (for example local structured blocks with an unstructured remainder, or prism layers with tetrahedral/polyhedral cells). Preserve structured regions where practical. A missing tool is a tooling limitation, not proof that the geometry cannot be structured; do not silently default to tetrahedral/polyhedral/hexcore methods. Do not call an all-hexahedral, hex-dominant or hexcore mesh structured without confirming its topology.

Record the feasibility assessment, selected method, any fallback reason and quality checks in the mesh result/report. Apply this preference to every newly meshed geometry variant and all grid-study levels; keep refinement topology/method consistent where possible. Reading or postprocessing an existing mesh alone does not authorize replacing it. A later explicit user choice overrides this default.
