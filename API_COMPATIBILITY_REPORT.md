# StormSense AI API Compatibility Report

## Scope

Persistence has been migrated from hardcoded MySQL access to an environment-driven Supabase PostgreSQL layer. API response shapes and scientific computation paths are preserved.

## Endpoint Compatibility Matrix

| Workflow | Endpoint / Surface | Persistence Impact | Status |
|---|---|---|---|
| Live Doppler | `/forecast`, websocket `/stream/atmospheric` | Forecast rows saved to PostgreSQL when `DATABASE_URL` is configured | Compatible |
| AI Prediction | `/forecast`, `/trend-analysis`, `/storm-escalation` | Scientific calculations unchanged | Compatible |
| Convective Analytics | frontend analytics modules | Reads existing API data; no DB contract change | Compatible |
| Historical Archive | `/cwc/historical-dates`, `/cwc/historical-observations`, `/cwc/historical-analysis` | Excel/archive driven; no MySQL dependency | Compatible |
| File Analysis Center | `/cwc/analyze-historical-dataset` | Upload parsing unchanged; Supabase table/storage schema prepared | Compatible |
| Forecast Verification | `/cwc/research-verification`, `/cwc/export/analysis` | Verification calculations unchanged | Compatible |
| Reviewer Dashboard | review mode/frontend review deck | JWT/auth shape preserved | Compatible |
| Dataset Explorer | archive/API data surfaces | No DB response shape changes | Compatible |
| Authentication | `/auth/signup`, `/auth/login`, `/auth/me` | Uses PostgreSQL `users` table; JWT payload unchanged | Compatible with configured `DATABASE_URL` |
| System Status | `/system-status` | Reports PostgreSQL/Supabase pool status instead of MySQL pool | Compatible |

## Preserved Contracts

- `/auth/login` still returns `{ token, user }`
- `/history` still returns a list of forecast rows with `station`, `cape`, `lifted_index`, `sweat_index`, `k_index`, `pwat`, `forecast`, `storm_probability`, `created_at`
- Forecast persistence remains best-effort and does not block forecast generation
- Websocket payload shape remains compatible; the earlier initial `telemetry_status` frame remains additive

## Required Production Configuration

- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

## Compatibility Decision

API-compatible for Phase 6.0 migration, provided production environments set `DATABASE_URL`.
