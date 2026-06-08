# Requirements Specification

Generated: 2026-06-08

## Functional Requirements

| ID | Requirement | Description | Evidence | Status |
| --- | --- | --- | --- | --- |
| FR-01 | Authentication | Allow users to log in and validate the active profile. | `/auth/login`, `/auth/me`, `backend/main.py` | Implemented |
| FR-02 | Historical archive search | Filter and inspect 2023-2025 thunderstorm records. | `/cwc/historical-dates`, `ResearchHub.jsx` | Implemented |
| FR-03 | Forecast simulation | Run station/custom sounding forecast reproduction. | `/forecast`, `ResearchHub.jsx:FORECAST_LAB` | Implemented |
| FR-04 | File analysis | Upload CSV/XLS/XLSX/radiosonde datasets and generate audit/registry output. | `/cwc/analyze-historical-dataset` | Implemented |
| FR-05 | Verification | Compute contingency metrics and threshold research. | `/cwc/verification`, `/cwc/threshold-research` | Implemented |
| FR-06 | Dataset explorer | Display archive coverage and CAPE dynamicity evidence. | `ResearchHub.jsx:DATASET_EXPLORER` | Implemented |
| FR-07 | Reviewer dashboard | Produce review docket, verdict, and export outputs. | `ResearchHub.jsx:REVIEWER_DASHBOARD` | Implemented |
| FR-08 | Live radar/nowcast | Display radar-like monitoring and coastal nowcast panels. | `RadarConsole.jsx`, `Phase3OpsModule.jsx` | Implemented |
| FR-09 | Bulletin generation | Generate operational bulletin products. | `/cwc/operational-bulletins` | Implemented |
| FR-10 | Single URL deployment | Serve React frontend and API from one Render service. | `backend/main.py`, `render.yaml` | Implemented |

## Non-Functional Requirements

| ID | Category | Requirement | Validation |
| --- | --- | --- | --- |
| NFR-01 | Reliability | Backend should import safely under `uvicorn backend.main:app` and preserve API endpoints. | Render deployment validation |
| NFR-02 | Determinism | Forecast, CAPE, probability, and verification outputs must remain deterministic and cycle-aware. | Engine audit and endpoint regression |
| NFR-03 | Security | Secrets must be environment-based; no database credentials hardcoded in source. | .env.example and deployment audit |
| NFR-04 | Performance | Operational pages should load without nested scroll failures and use API polling/websocket responsibly. | Frontend build and browser review |
| NFR-05 | Maintainability | Frontend modules and backend engines must preserve existing ownership boundaries. | Source reference matrix |
| NFR-06 | Scalability | Persistence layer should use Supabase PostgreSQL and SQLAlchemy connection pooling. | Supabase migration reports |
| NFR-07 | Availability | Static frontend and API fallback should share one deployed service with SPA route refresh support. | Single URL deployment report |
| NFR-08 | Accessibility | Operational labels, status text, and controls should remain readable and keyboard-auditable. | Accessibility audit |

## Traceability Note
Requirements are derived from supplied screenshots, `frontend/src` modules, FastAPI route decorators, Supabase schema, and generated migration/deployment reports.

