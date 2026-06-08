# Testing Report

Generated: 2026-06-08

| Test Area | Method | Acceptance Condition |
| --- | --- | --- |
| Build | `npm run build` | Generate `frontend/dist` for single-URL Render deployment. |
| Backend import | `python -c "import backend.main"` | No `ModuleNotFoundError` under package startup. |
| API smoke | `/system-status`, `/history`, `/forecast`, `/cwc/historical-dates` | HTTP 200 JSON response and stable schema. |
| Websocket | `/stream/atmospheric` | Receive operational telemetry frame or graceful fallback. |
| Upload | `/cwc/analyze-historical-dataset` | Quality summary, station/parameter detection, registry, and export metadata. |
| Archive | Historical Thunderstorm Archive UI | 2023, 2024, 2025 records participate in summaries and registry. |
| Verification | Threshold verification lab | CSI, POD, FAR, HSS, BIAS computed from historical observations. |
| Review Mode | Header Review Mode toggle | Reviewer-critical fields visible; diagnostics hidden. |
| Deployment | Render single URL | Root and browser routes serve React shell; APIs remain active. |

## Detailed Test Scenarios

### Authentication Testing
POST `/auth/login` with a known reviewer account, verify token issuance, store token in frontend local storage, call `/auth/me`, then logout and confirm protected actions are unavailable.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### Historical Archive Testing
Open Research & Insights -> Historical Thunderstorm Archive. Confirm 2023, 2024, and 2025 records are visible in summaries, latest thunderstorm calculation, registry filters, and historical analysis.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### File Upload Testing
Upload CSV/XLS/XLSX files through Analyze Historical Dataset. Confirm station detection, parameter detection, missing values, duplicate rows, quality score, registry generation, and latestFileAnalyzed update.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### Forecast Simulator Testing
Run the simulator for Visakhapatnam and Machilipatnam. Confirm deterministic outputs, threshold trace, probability explanation, forecast result, and verification result.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### Verification Testing
Run threshold research by station/season and verify CSI, HSS, POD, FAR, and BIAS change deterministically with threshold input.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### CAPE Traceability Testing
Call `/cwc/cape-traceability`, check NOW through T-6 timeline, source status, cache age, delta CAPE, and STATIC_DATA_WARNING behavior.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### SPA Deployment Testing
Open Render URL at `/`, `/dashboard`, `/research`, `/archive`, and `/forecast`. Refresh each route and confirm React shell loads.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### API Preservation Testing
Call `/system-status`, `/history`, `/forecast`, `/cwc/historical-dates`, and `/cwc/historical-analysis`. Confirm JSON payloads remain active after static frontend serving.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### Websocket Testing
Connect to `/stream/atmospheric` and verify forecast/trend/escalation/cycle frames arrive or fall back cleanly.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.

### Reviewer Acceptance Testing
Enable IMD Review Mode and confirm the reviewer sees date, time, station, observed event, forecast result, verification result, meteorologist summary, and recommended action without diagnostics clutter.
Expected outcome: pass/fail result must be recorded with endpoint, UI location, dataset/source, and reviewer-visible evidence.


