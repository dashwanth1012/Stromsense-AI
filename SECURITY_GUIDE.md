# Security Guide

Generated: 2026-06-08

| Security Area | Current Evidence | Production Control |
| --- | --- | --- |
| Authentication | `/auth/login`, `/auth/signup`, `/auth/me` in FastAPI. | Validate password hashing policy and token expiry in deployment. |
| Authorization | Bearer-token flow used by authenticated profile checks. | Add route-level policy audit for production roles. |
| Secrets | Database/Supabase credentials are environment variables; `.env.example` documents required keys. | Never commit `.env` values. |
| Database | Supabase PostgreSQL schema and SQLAlchemy connection layer. | Review RLS/Supabase policies before external launch. |
| File uploads | File analysis endpoint supports CSV/XLS/XLSX/radiosonde datasets. | Limit file size, validate MIME/type, sanitize names, and scan inputs as deployment policy. |
| CORS | CORS allow-list can be set through environment policy. | Restrict production origins. |
| Audit logs | Migration/auth audit tables exist in schema. | Verify log retention and PII policy. |

## Deployment Rule
Use environment variables only for database URLs, Supabase keys, JWT secrets, and deployment origins. Do not hardcode credentials in frontend or backend source files.

