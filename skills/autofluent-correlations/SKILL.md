---
name: autofluent-correlations
description: Select applicable circular-tube heat-transfer correlations and calculate Nu and h with explicit validity reasons. 用于 Dittus–Boelter Gnielinski 层流与入口段理论比较。
---

# 理论关联式比较

## Runtime

Requires AutoFluent MCP 0.3.0 (36 tools), Fluent 2023 R1 and PyFluent 0.37.0 for solver operations. Call fluent_diagnostics and fluent_sessions first when a solver is needed. Reuse an idle, appropriate session; use the installed autofluent-gui skill only when a visible window is requested. If the new tool is missing, reconnect the upgraded MCP; do not claim it ran.

Poll every returned job_id with fluent_job_status until terminal. A succeeded job does not prove convergence or applicability. Use new workspace-relative output directories. Preserve unsaved case changes before loading another case or initializing. Never print or publish server-info credentials. Read references/example.json for the argument structure, replacing model-specific values from the actual case.

## Workflow

Call fluent_heat_transfer_correlations; no solver is required. Derive Re and Pr from actual bulk properties and velocity, and provide diameter, conductivity, heated length, smoothness, hydrodynamic/thermal development, wall boundary type and heating/cooling direction. Do not mark fully developed solely because the solver converged.

The tool returns Dittus-Boelter, Gnielinski, fully developed laminar and Hausen mean thermal-entry results. Inapplicable entries return null Nu/h and specific reasons. Hausen is for hydrodynamically developed laminar constant-wall-temperature flow; fully developed laminar values differ between constant Tw and constant heat flux. Transitional flow is uncertain even when inside a broad empirical range. Constant-property smooth circular-tube assumptions exclude roughness, noncircular passages and large property changes.

Compare like definitions: local versus length-mean h/Nu and consistent reference properties. Quote the returned formulas and sources. These empirical references are not exact theoretical solutions. Use the existing Excel workflow for the original nine-column request; do not label its Dittus-Boelter-only output as containing all four correlations.

## Clarify the workflow before choosing a plan

Before proposing or materially changing an end-to-end workflow, check the user's existing instructions and inspect available inputs. Promptly ask about unresolved facts or choices that change the physics, method, cost, validation or deliverables. Use workflow-plan-clarify when available. Ask only the relevant missing questions, offer reasoned alternatives, and wait for required answers before dependent work; continue independent checks meanwhile. Do not re-ask settled questions or impose an extra approval step when the plan is already clear.
