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

## Meshing preference — structured first

For every new mesh or remeshing task, first assess structured meshing feasibility from the actual geometry and topology. Prefer mapped quadrilateral meshes in 2D and mapped/swept or multiblock hexahedral meshes in 3D when feasible. Consider reasonable partitioning, sweep source/target compatibility and pipe O-grid/block layouts before abandoning the structured route. Verify mesh quality and near-wall resolution; do not force a poor structured mesh merely to satisfy the preference.

Use another method only after identifying why the structured approach is unsuitable or unavailable. State the specific geometric/topological, quality or tooling limitation, then select a suitable alternative (for example local structured blocks with an unstructured remainder, or prism layers with tetrahedral/polyhedral cells). Preserve structured regions where practical. A missing tool is a tooling limitation, not proof that the geometry cannot be structured; do not silently default to tetrahedral/polyhedral/hexcore methods. Do not call an all-hexahedral, hex-dominant or hexcore mesh structured without confirming its topology.

Record the feasibility assessment, selected method, any fallback reason and quality checks in the mesh result/report. Apply this preference to every newly meshed geometry variant and all grid-study levels; keep refinement topology/method consistent where possible. Reading or postprocessing an existing mesh alone does not authorize replacing it. A later explicit user choice overrides this default.

## Clarify the workflow before choosing a plan

Before proposing or materially changing an end-to-end workflow, check the user's existing instructions and inspect available inputs. Promptly ask about unresolved facts or choices that change the physics, method, cost, validation or deliverables. Use workflow-plan-clarify when available. Ask only the relevant missing questions, offer reasoned alternatives, and wait for required answers before dependent work; continue independent checks meanwhile. Do not re-ask settled questions or impose an extra approval step when the plan is already clear.
