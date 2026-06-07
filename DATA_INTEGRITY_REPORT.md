# Data Integrity Report

## Result

Status: Not validated against Supabase target.

## Planned Integrity Checks

| Check | Status |
|---|---|
| Primary keys | Pending database connection |
| Foreign keys | Pending database connection |
| Unique constraints | Pending database connection |
| Indexes | Pending database connection |
| User count parity | Pending database connection |
| Forecast count parity | Pending database connection |
| Duplicate ID detection | Pending database connection |

## Local Static Integrity

- MySQL export parser successfully reads expected source records.
- PostgreSQL schema defines primary keys and indexes.
- `users.email` unique constraint is preserved.
- `thunderstorm_forecasts.id` identity/primary key is preserved.

