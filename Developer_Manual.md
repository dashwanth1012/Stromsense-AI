# StormSense AI Developer Manual

## Project Structure

| Area | Path | Responsibility |
| --- | --- | --- |
| Frontend entry | frontend/src/App.jsx | Authentication, global telemetry state, websocket connection, and workstation module routing. |
| Sidebar | frontend/src/components/layout/Sidebar.jsx | Primary navigation module list. |
| Research center | frontend/src/components/modules/ResearchHub.jsx | Start Here, About, archive, simulator, verification, dataset explorer, reviewer dashboard, index guide, terminology. |
| Phase 3 ops modules | frontend/src/components/modules/Phase3OpsModule.jsx | Atmospheric intelligence, watchdesk, lab, bulletin, analog, Andhra monitoring, verification. |
| Backend app | backend/main.py | FastAPI routes, authentication, websocket, forecasting, archive endpoints, file upload endpoints, static SPA serving. |
| Research engines | backend/analysis_engines.py | Historical observations, verification, probability, climatology, analog, district impact, bulletins. |
| Thermodynamics | backend/thermo.py | Sounding parsing and thermodynamic solver. |
| Sounding ingestion | backend/fetch_sounding.py | Wyoming fetch, cache metadata, freshness scoring, cycle-aware cache. |
| Database layer | backend/database.py and backend/connection_pool.py | SQLAlchemy PostgreSQL connection and Supabase schema initialization helpers. |

## Local Development
1. Install backend requirements from `backend/requirements.txt`.
2. Install frontend dependencies from `frontend/package.json`.
3. Set `.env` values for Supabase/PostgreSQL and authentication secrets.
4. Run FastAPI with `uvicorn backend.main:app` from the repository root.
5. Run `npm run dev` in `frontend/` only for local frontend development; production uses FastAPI static serving.

## Code Organization Rules
- Keep scientific functions in `analysis_engines.py`, `thermo.py`, and `fetch_sounding.py` deterministic.
- Keep UI refinements inside existing components unless a component already owns the workflow.
- Do not hardcode deployment URLs in frontend code; production resolves same-origin through `environment.js`.
- Preserve package-safe backend imports because Render starts `uvicorn backend.main:app`.

## Database Migration
- Supabase schema is maintained in `supabase_schema.sql`.
- Migration execution is handled by `migration_runner.py`.
- Runtime database access uses SQLAlchemy through `backend/database.py` and `backend/connection_pool.py`.

## Contribution Guidelines
- Run frontend build before deployment handoff.
- Run backend import and compile validation after backend changes.
- Preserve CAPE, probability, verification, and archive determinism.
- Add documentation evidence for any new operational module or endpoint.
