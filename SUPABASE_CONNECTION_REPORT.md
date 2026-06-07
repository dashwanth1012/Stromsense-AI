# Supabase Connection Report

## Result

Status: Blocked before schema apply.

## Validated Inputs

- `DATABASE_URL` is present in local `.env`.
- Credentials were loaded from environment variables only.
- Source files were not updated with hardcoded credentials.
- SSL mode was requested with `sslmode=require`.

## Connection Checks

| Check | Result |
|---|---|
| DNS resolution for direct DB host | Passed |
| Direct DB host address family | IPv6 only |
| Direct TCP connection to `5432` | Failed from this machine |
| Direct PostgreSQL SSL connection | Failed due TCP timeout |
| Pooler host reachability | IPv4 pooler hosts reachable |
| Pooler tenant recognition | Failed; tenant identifier not found on probed pooler hosts |

## Blocking Error

```text
connection to server at "db.mkwjqevginxpqdcgmzch.supabase.co", port 5432 failed: Connection timed out
```

## Interpretation

The official direct Supabase PostgreSQL host resolves to an IPv6 address only in this environment. This Windows network path cannot reach that IPv6 endpoint. The generic Supabase pooler hosts are reachable over IPv4, but the project tenant was not recognized using the standard inferred pooler user format.

## Required Remediation

Use one of the following:

- Enable IPv6 connectivity on this machine/network and rerun `migration_runner.py --apply`.
- Provide the exact Supabase connection pooler string from Project Settings > Database > Connection pooling.

