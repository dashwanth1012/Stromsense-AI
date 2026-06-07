# Migration Apply Report

## Result

Status: Not applied.

## Actions Attempted

1. Loaded `DATABASE_URL` from local environment configuration.
2. Validated direct Supabase PostgreSQL connection with SSL required.
3. Probed Supabase pooler transport because direct host is IPv6-only.

## Schema Apply Status

| Object Type | Status |
|---|---|
| PostgreSQL tables | Not created in Supabase target |
| Constraints | Not applied |
| Indexes | Not applied |
| Relationships | Not applied |
| Storage buckets | Not created |

## Cause

The migration runner could not establish a PostgreSQL session with the target Supabase database.

## Ready-To-Run Command After Connectivity Fix

```powershell
cd "C:\Users\USER\Thunderstorm analysis"
$env:DATABASE_URL = (Get-Content .env | Where-Object { $_ -like 'DATABASE_URL=*' } | Select-Object -First 1).Substring('DATABASE_URL='.Length)
backend\venv\Scripts\python.exe migration_runner.py --apply --summary MIGRATION_TEST_REPORT.supabase.json
```

