# API Validation Report

Validation target: `http://127.0.0.1:8010`

## Endpoint Results

- `/` - HTTP 200, backend health message returned.
- `/system-status` - HTTP 200, backend status `ONLINE`, database status `CONNECTED`, active stations `5`.
- `/history` - HTTP 200, returned 100 latest forecast-history rows from `thunderstorm_forecasts`.
- `/forecast` - HTTP 200, returned 5 station forecasts and persisted the validation cycle to Supabase.
- `/auth/login` - HTTP 200, migrated `chief@stormsense.gov.in` user authenticated as `MET_CHIEF`.
- `/cwc/historical-dates` - HTTP 200, returned 360 historical archive records.
- `/cwc/historical-analysis?date=2025-06-24&station=Visakhapatnam` - HTTP 200, returned historical analysis, district impacts, probability traceability, and verification metrics.

## Persistence Evidence

- Imported Workbench forecast rows: 942.
- Post-validation forecast table count: 947.
- Difference: 5 rows written by the `/forecast` endpoint during API validation.
- User records persisted in Supabase: 3.
- Historical observations persisted in Supabase: 360.

Result: Required backend endpoints are compatible with the Supabase PostgreSQL persistence layer.
