# Native contours and heated pipe studies

Requires AutoFluent MCP 0.2.0, Fluent 2023 R1 and PyFluent 0.37.0. All four tools return jobs: poll fluent_job_status until terminal. Reconnect the MCP after upgrading; verify all four names are present before claiming availability.

## 1. Native contours

Call fluent_render_contour with session_id, a new workspace-relative output PNG and spec:

```json
{"field":"y-velocity","plane":"yz-plane","coordinate":0,"view":"left","roll_degrees":90,"minimum":0,"maximum":20,"width":1600,"height":900}
```

This example assumes flow along Y and a centre plane at X=0. Inspect actual geometry first. Specify existing surfaces instead of plane when appropriate. Supply both minimum and maximum for a shared scale; omit both for automatic range. zoom defaults to 1. This updates Fluent's native graphics and saves a snapshot. It does not embed or stream the desktop. A plane can intersect solid zones as well as fluid.

## 2. Batch velocities and recovery

Call fluent_run_pipe_study with session_id, base_case, directory, velocities, pipe, criteria and optional contour. Example velocities: [1,3,5,7,9,11,13,15]. resume and export default to true.

The workflow reloads the base case and hybrid-initializes each new attempt. Save existing unsaved work first. It preserves the base case physics except inlet velocity and its named monitoring reports. It supports a steady, single-inlet/single-outlet heated pipe with constant properties, no additional heat paths or sources. Inspect these assumptions; they are not all automatically detected.

pipe fields: inlet, outlet, inner_wall, heated_wall, fluid_zone, diameter (m), heated_length (m), density (kg/m3), viscosity (Pa s), conductivity (W/m K), specific_heat (J/kg K). Defaults are inlet/outlet/innerwall/outwall/fluid and 0.01/1/1000/0.001/0.6/4182. Set actual model values explicitly. Material constants must match Fluent. The heated_wall is the heat-input boundary; inner_wall is the fluid heat-transfer surface.

manifest.json records configuration, attempts, statuses and SHA256 checksums. Repeat with the same directory/settings and an expanded velocity list: only verified complete cases are skipped. Changed base/settings require a new directory. Interrupted or unconverged cases start new attempts; old attempts remain. Recovery is at case level, not from the last iteration. A crash may leave .study.lock: inspect active processes/jobs before removing a confirmed stale lock. Never remove an active lock. A plotting failure can mark an attempt interrupted even if solution files exist.

## 3. Combined convergence

fluent_iterate_until_converged accepts session_id, output (new JSON path), pipe and criteria. It continues the loaded solution without initializing it. The batch tool uses the same checker.

Default criteria: min_iterations 150, max_iterations 1000, chunk_size 50, stable_checks 2; relative_h 0.001, mass_balance 0.00001, energy_balance 0.0001. residual_limits defaults to continuity, x/y/z-velocity, k, epsilon at 1e-6 and energy at 1e-9. Match the required residual names to the model (e.g. omega for SST); missing/nonfinite residuals fail the check. Iteration budgets count requested steps; Fluent can stop a chunk earlier. History includes the observed residual iteration number. Checks use transcript delivery and report values after each chunk, not every internal iteration.

Mass error = abs(m_in+m_out)/abs(m_in). Energy error compares m_in cp (Tout-Tin) with heated-wall heat input. h stability is relative change between checks. All checks must pass for the configured consecutive count. Reaching the budget returns converged=false / not_converged, even when the job itself succeeds. Cancellation is cooperative between chunks. Inspect history, wall y-plus and mesh suitability before treating a result as engineering validation.

## 4. Excel and theory comparison

fluent_export_study accepts directory and needs no solver session. Batch export runs automatically unless export=false; check export_error separately. Only complete cases whose result and solution checksums agree enter the workbook. Exclusions are reported.

The results sheet contains exactly q, Tw, Tf, k, d, h, Nu_cal, Re, Pr, sorted by velocity. The comparison sheet maps velocities and contains editable Nu and h charts. q is inner-wall heat flux (W/m2); Tw is area-averaged inner-wall temperature (K); Tf=(mass-averaged Tin+Tout)/2. h=q/(Tw-Tf), Nu=h*d/k, Re=rho*u*d/mu, Pr=cp*mu/k. This is a mean-temperature definition, not an LMTD calculation.

Theory uses Dittus-Boelter Nu=0.023 Re^0.8 Pr^0.4 for fluid heating in a smooth developed turbulent tube. The workbook only evaluates it when Re>=10000, 0.7<=Pr<=160 and heated_length/diameter>=10. Smoothness/development still require engineering judgement. No entrance correction is applied; values outside the numeric range are marked n.a. This empirical correlation is a reference, not an exact solution.

Excel authoring uses Codex's bundled Node and @oai/artifact-tool. Defaults discover the local Codex runtime; other environments must set AUTOFLUENT_NODE (executable) and AUTOFLUENT_ARTIFACT_MODULES (node_modules directory). No Fluent license is required to re-export saved verified results. Each export uses a new directory; latest-export.json points to the last successful export. Inspect returned workbook and PNG before delivery.
