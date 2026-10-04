---
name: autofluent-pressure
description: Measure Fluent pressure loss, Darcy/Fanning friction factors, hydraulic power and optional baseline-relative heat-transfer performance. 用于压降和综合热工性能评价。
---

# 压降与综合性能

## Runtime

Requires AutoFluent MCP 0.3.0 (36 tools), Fluent 2023 R1 and PyFluent 0.37.0 for solver operations. Call fluent_diagnostics and fluent_sessions first when a solver is needed. Reuse an idle, appropriate session; use the installed autofluent-gui skill only when a visible window is requested. If the new tool is missing, reconnect the upgraded MCP; do not claim it ran.

Poll every returned job_id with fluent_job_status until terminal. A succeeded job does not prove convergence or applicability. Use new workspace-relative output directories. Preserve unsaved case changes before loading another case or initializing. Never print or publish server-info credentials. Read references/example.json for the argument structure, replacing model-specific values from the actual case.

## Workflow

Call fluent_pressure_performance on a converged solution. Supply inlet/outlet sampling surfaces, measured separation length, diameter, density and viscosity. For friction-factor interpretation use constant-area, straight, horizontal, developed-flow sections; fittings, gravity, acceleration and entry losses otherwise contaminate the result.

The tool area-averages static pressure, mass-averages total pressure, and obtains inlet mass flow and area. U=mdot/(rho A), Darcy f=dp_static D/(L rho U²/2), Fanning f=Darcy/4. Hydraulic power=(pt_in-pt_out)Q; it excludes pump efficiency. Negative drops remain signed evidence, not silently made positive.

PEC is optional: provide nu, reference_nu, reference_darcy and comparable_reference=true only when baseline geometry, definitions and comparison basis justify PEC=(Nu/Nu0)/(f/f0)^(1/3). This convention does not prove equal-pumping-power equivalence for arbitrary geometries. Missing baseline yields null PEC. Report averaging and pressure definitions with units.

## Clarify the workflow before choosing a plan

Before proposing or materially changing an end-to-end workflow, check the user's existing instructions and inspect available inputs. Promptly ask about unresolved facts or choices that change the physics, method, cost, validation or deliverables. Use workflow-plan-clarify when available. Ask only the relevant missing questions, offer reasoned alternatives, and wait for required answers before dependent work; continue independent checks meanwhile. Do not re-ask settled questions or impose an extra approval step when the plan is already clear.
