# StormSense AI Migration Test Report

## Static Validation

| Check | Result |
|---|---|
| MySQL dump readable | Passed |
| PostgreSQL schema generated | Complete |
| Migration runner generated | Complete |
| FastAPI PostgreSQL connection layer generated | Complete |
| Hardcoded MySQL credentials removed from backend Python | Passed |
| Supabase storage bucket SQL generated | Complete |
| Backend `py_compile` | Passed |
| Frontend `npm run build` | Passed |
| API/upload smoke without `DATABASE_URL` | Passed |
| Websocket smoke | Passed |

## Dry-Run Migration Results

Command:

```powershell
backend\venv\Scripts\python.exe migration_runner.py
```

Result:

| Table | Parsed Rows | Applied |
|---|---:|---|
| `users` | 3 | No, dry run only |
| `thunderstorm_forecasts` | 942 | No, dry run only |

Optional operational tables were not present in the supplied MySQL export and will be created empty by `supabase_schema.sql`.

## API Smoke Results

Validated after PostgreSQL layer integration:

| Endpoint | Result |
|---|---|
| `/` | HTTP 200 |
| `/history` | HTTP 200 |
| `/forecast` | HTTP 200 |
| `/system-status` | HTTP 200 |
| `/cwc/historical-dates` | HTTP 200 |
| `/cwc/historical-observations` | HTTP 200 |
| `/cwc/cape-traceability` | HTTP 200 |
| `/cwc/latest-file-analyzed` | HTTP 200 |
| `/cwc/analyze-historical-dataset` upload | HTTP 200 |
| `/stream/atmospheric` websocket | `WEBSOCKET_OK` |

The local smoke was run without production `DATABASE_URL`; `/history` correctly returned an empty list rather than attempting MySQL fallback.

## Runtime Validation To Perform With Supabase Credentials

1. Set `DATABASE_URL`.
2. Run `backend\venv\Scripts\python.exe migration_runner.py --apply`.
3. Confirm migration output:
   - `users.expected = 3`
   - `users.actual >= 3`
   - `thunderstorm_forecasts.expected = 942`
   - `thunderstorm_forecasts.actual >= 942`
4. Start backend.
5. Verify endpoints:
   - `/history`
   - `/forecast`
   - `/auth/login`
   - `/system-status`
6. Upload `scratch/sample_historical_upload.csv` to `/cwc/analyze-historical-dataset`.
7. Verify websocket `/stream/atmospheric`.

## Supabase Production Connection Attempt

Date: 2026-06-07

Result:

| Check | Result |
|---|---|
| Supabase host reachable | Yes |
| Direct PostgreSQL SSL connection attempted | Yes |
| URL-encoded `DATABASE_URL` attempt | Failed authentication |
| Keyword-parameter `host/user/password` attempt | Failed authentication |
| User-provided encoded `DATABASE_URL` attempt | Failed authentication |
| Credentials written to source | No |
| Migration applied to Supabase | No |

Blocking error:

```text
FATAL: password authentication failed for user "postgres"
```

Interpretation:

The database host is reachable, but Supabase rejected the supplied database password for the `postgres` user. Re-run `migration_runner.py --apply` after confirming the current database password in Supabase Project Settings.

Latest attempted environment-only connection format:

```text
DATABASE_URL=postgresql://postgres:<redacted>@db.mkwjqevginxpqdcgmzch.supabase.co:5432/postgres?sslmode=require
```

## Notes

No production Supabase credentials were present in this workspace at generation time, so apply-mode database validation must be run after `DATABASE_URL` is supplied.
