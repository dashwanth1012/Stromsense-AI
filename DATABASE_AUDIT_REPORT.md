# StormSense AI Database Audit Report

## Source

- MySQL export directory: `C:\Users\USER\Documents\dumps\Dump20260607`
- Export files:
  - `stormsense_db_users.sql`
  - `stormsense_db_thunderstorm_forecasts.sql`
- Source database name in dump: `stormsense_db`
- Dump completed: `2026-06-07 21:42:57`

## Tables

| Table | Records In Export | Primary Key | Indexes | Foreign Keys | Triggers | Views |
|---|---:|---|---|---|---|---|
| `users` | 3 | `id` | unique `email` | none | none | none |
| `thunderstorm_forecasts` | 942 | `id` | none in MySQL export | none | none | none |

## Table Details

### `users`

Columns:

- `id INT AUTO_INCREMENT NOT NULL`
- `name VARCHAR(255) NOT NULL`
- `email VARCHAR(255) NOT NULL`
- `password VARCHAR(255) NOT NULL`
- `role VARCHAR(100) NOT NULL`
- `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`

Constraints:

- Primary key on `id`
- Unique key on `email`

### `thunderstorm_forecasts`

Columns:

- `id INT AUTO_INCREMENT NOT NULL`
- `station VARCHAR(255)`
- `station_code VARCHAR(255)`
- `cape FLOAT`
- `lifted_index FLOAT`
- `sweat_index FLOAT`
- `k_index FLOAT`
- `pwat FLOAT`
- `forecast VARCHAR(255)`
- `storm_probability INT`
- `created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP`

Constraints:

- Primary key on `id`

## Backend Dependencies Found

Current persistence usage before migration was concentrated in:

- Authentication: `/auth/signup`, `/auth/login`, `/auth/me`
- Forecast persistence: `thunderstorm_forecasts`
- Forecast history: `/history`
- System health metadata: `/system-status`

Historical archive, CAPE traceability, verification engines, file analysis, and operational forecast logic are not dependent on the MySQL dump schema.

## Migration Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Supabase `DATABASE_URL` missing in production | High | `.env.example` created; backend now reports `UNCONFIGURED` instead of hardcoded localhost MySQL |
| User passwords are SHA-256 hashes, not Supabase Auth hashes | Medium | Preserve legacy users table for compatibility; `profiles`, `roles`, and `audit_login` added for Supabase migration path |
| `thunderstorm_forecasts` contains duplicate operational forecast cycles | Low | Preserve all IDs and rows exactly; no deduplication performed |
| Cold `/forecast` endpoint can be slow due live sounding resolution | Medium | No scientific logic changed; operational smoke uses longer timeout |
| Optional operational tables were not present in MySQL dump | Low | Supabase schema creates empty operational tables for uploaded datasets, registry, verification, review records, and audit logs |

## Decision

The MySQL export is structurally simple and safe to migrate. No foreign key, trigger, or view dependency blocks Supabase PostgreSQL migration.
