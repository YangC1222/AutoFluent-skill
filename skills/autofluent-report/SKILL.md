---
name: autofluent-report
description: Generate evidence-backed Word and PDF reports from Fluent preflight convergence results plots and theory analyses. 用于整理可追溯的仿真报告。
---

# 自动仿真报告

## Runtime

Requires AutoFluent MCP 0.3.0 (36 tools), Fluent 2023 R1 and PyFluent 0.37.0 for solver operations. Call fluent_diagnostics and fluent_sessions first when a solver is needed. Reuse an idle, appropriate session; use the installed autofluent-gui skill only when a visible window is requested. If the new tool is missing, reconnect the upgraded MCP; do not claim it ran.

Poll every returned job_id with fluent_job_status until terminal. A succeeded job does not prove convergence or applicability. Use new workspace-relative output directories. Preserve unsaved case changes before loading another case or initializing. Never print or publish server-info credentials. Read references/example.json for the argument structure, replacing model-specific values from the actual case.

## Workflow

Install the MCP reports extra for Word/PDF generation. Gather actual analysis result.json files and study manifest.json files from preflight, convergence/studies, axial, pressure, grid and theory tasks. Missing evidence should be listed as unverified; do not run new simulations unless the request calls for them.

Call fluent_engineering_report with sources (1..10 workspace-relative JSON files), a new directory, title and optional notes. Study manifests are checksum-verified and incomplete/corrupt cases are excluded. Other analysis files are preserved with SHA256 in evidence.json; hashing establishes provenance, not correctness. Compact tables may truncate long lists; full supplied evidence is retained separately.

Include mesh/model/convergence evidence when available, state physical assumptions and comparison limitations in notes, and identify which requested checks remain absent. The exporter includes axial.png beside an axial result. It produces editable report.docx, report.pdf and evidence.json. Avoid including credential files or unrelated personal paths as sources.

Render the DOCX with the available document renderer and inspect every page; render the PDF and inspect every page too. Correct clipping, unsupported glyphs or broken tables before delivery. If a renderer is unavailable, state that limitation instead of calling the report visually verified. Generated results are engineering evidence summaries, not certified validation reports.

## Clarify the workflow before choosing a plan

Before proposing or materially changing an end-to-end workflow, check the user's existing instructions and inspect available inputs. Promptly ask about unresolved facts or choices that change the physics, method, cost, validation or deliverables. Use workflow-plan-clarify when available. Ask only the relevant missing questions, offer reasoned alternatives, and wait for required answers before dependent work; continue independent checks meanwhile. Do not re-ask settled questions or impose an extra approval step when the plan is already clear.
