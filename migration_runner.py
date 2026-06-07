import argparse
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent


def _find_env_file(start: Path) -> Path | None:
    for directory in (start, *start.parents):
        candidate = directory / ".env"
        if candidate.exists():
            return candidate
    return None


DOTENV_PATH = _find_env_file(ROOT)
DOTENV_LOADED = False
try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - dotenv is validated by the migration command
    load_dotenv = None

if load_dotenv and DOTENV_PATH:
    DOTENV_LOADED = bool(load_dotenv(DOTENV_PATH))

DEFAULT_DUMP_DIR = Path(os.getenv("MYSQL_DUMP_DIR", r"C:\Users\USER\Documents\dumps\Dump20260607"))

TABLE_EXPORTS = {
    "users": {
        "file": "stormsense_db_users.sql",
        "columns": ["id", "name", "email", "password", "role", "created_at"],
    },
    "thunderstorm_forecasts": {
        "file": "stormsense_db_thunderstorm_forecasts.sql",
        "columns": [
            "id",
            "station",
            "station_code",
            "cape",
            "lifted_index",
            "sweat_index",
            "k_index",
            "pwat",
            "forecast",
            "storm_probability",
            "created_at",
        ],
    },
}

OPTIONAL_TABLES_NOT_IN_EXPORT = [
    "historical_observations",
    "historical_records",
    "thunderstorm_registry",
    "verification_results",
    "uploaded_datasets",
    "reviewer_dashboard_records",
    "audit_logs",
    "roles",
    "profiles",
    "audit_login",
]

VALIDATION_TABLES = [
    "users",
    "thunderstorm_forecasts",
    "historical_observations",
    "historical_records",
    "thunderstorm_registry",
    "uploaded_datasets",
    "verification_results",
    "reviewer_dashboard_records",
]


def _postgres_url(url: str) -> str:
    if url.startswith("postgresql+psycopg2://"):
        return "postgresql://" + url[len("postgresql+psycopg2://"):]
    return url


def _redact_url(url: str) -> str:
    return re.sub(r":([^:@/?#]+)@", ":***@", url or "")


def emit_environment_diagnostics():
    print("DOTENV LOADED")
    print("DOTENV PATH =", str(DOTENV_PATH) if DOTENV_PATH else "NOT FOUND")
    print("DATABASE_URL =", _redact_url(os.getenv("DATABASE_URL", "")))
    print("SUPABASE_DB_HOST =", os.getenv("SUPABASE_DB_HOST", ""))


def _read_dump(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def extract_insert_values(sql_text: str, table: str) -> str:
    pattern = re.compile(rf"INSERT INTO `{re.escape(table)}` VALUES\s*(.*?);", re.IGNORECASE | re.DOTALL)
    match = pattern.search(sql_text)
    return match.group(1).strip() if match else ""


def iter_tuple_text(values_blob: str):
    depth = 0
    in_quote = False
    escape = False
    start = None
    for idx, char in enumerate(values_blob):
        if escape:
            escape = False
            continue
        if in_quote and char == "\\":
            escape = True
            continue
        if char == "'":
            in_quote = not in_quote
            continue
        if in_quote:
            continue
        if char == "(":
            if depth == 0:
                start = idx
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and start is not None:
                yield values_blob[start:idx + 1]
                start = None


def parse_mysql_tuple(tuple_text: str) -> list[Any]:
    body = tuple_text.strip()[1:-1]
    values: list[str] = []
    current: list[str] = []
    in_quote = False
    escape = False
    for char in body:
        if escape:
            current.append(char)
            escape = False
            continue
        if in_quote and char == "\\":
            escape = True
            continue
        if char == "'":
            in_quote = not in_quote
            continue
        if char == "," and not in_quote:
            values.append("".join(current))
            current = []
            continue
        current.append(char)
    values.append("".join(current))
    return [coerce_value(value) for value in values]


def coerce_value(value: str) -> Any:
    raw = value.strip()
    if raw.upper() == "NULL":
        return None
    if raw == "":
        return ""
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if re.fullmatch(r"-?\d+\.\d+", raw):
        return float(raw)
    return raw


def load_table_records(dump_dir: Path, table: str) -> list[dict[str, Any]]:
    config = TABLE_EXPORTS[table]
    path = dump_dir / config["file"]
    if not path.exists():
        return []
    blob = extract_insert_values(_read_dump(path), table)
    records = []
    for tuple_text in iter_tuple_text(blob):
        values = parse_mysql_tuple(tuple_text)
        records.append(dict(zip(config["columns"], values)))
    return records


def connect_to_supabase():
    try:
        import psycopg2
    except Exception as exc:  # pragma: no cover
        raise SystemExit("psycopg2-binary is required. Install backend/requirements.txt before applying migration.") from exc
    database_url = os.getenv("DATABASE_URL", "").strip()
    if database_url:
        return psycopg2.connect(_postgres_url(database_url))
    host = os.getenv("SUPABASE_DB_HOST", "").strip()
    password = os.getenv("SUPABASE_DB_PASSWORD", "")
    if not host or not password:
        print("ENV CHECK FAILED in connect_to_supabase")
        print("DATABASE_URL present =", bool(database_url))
        print("SUPABASE_DB_HOST present =", bool(host))
        print("SUPABASE_DB_PASSWORD present =", bool(password))
        raise SystemExit("DATABASE_URL or SUPABASE_DB_HOST/SUPABASE_DB_PASSWORD are required for apply mode.")
    user = os.getenv("SUPABASE_DB_USER", "postgres").strip()
    port = os.getenv("SUPABASE_DB_PORT", "5432").strip()
    name = os.getenv("SUPABASE_DB_NAME", "postgres").strip()
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=name,
        user=user,
        password=password,
        sslmode="require",
    )


def apply_schema(connection):
    schema_path = ROOT / "supabase_schema.sql"
    with connection.cursor() as cursor:
        cursor.execute(schema_path.read_text(encoding="utf-8"))
    connection.commit()


def _normalize_date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text[:10], fmt).date()
        except ValueError:
            continue
    return None


def load_historical_rows_for_migration() -> tuple[list[dict[str, Any]], str | None]:
    backend_path = ROOT / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    try:
        import analysis_engines

        rows = analysis_engines.load_historical_observations()
        return list(rows), None
    except Exception as exc:
        return [], str(exc)


def _history_insert_payload(row: dict[str, Any]):
    try:
        from psycopg2.extras import Json
    except Exception as exc:  # pragma: no cover
        raise SystemExit("psycopg2-binary is required for JSONB archive migration.") from exc
    return {
        "record_date": _normalize_date(row.get("date")),
        "observation_time": str(row.get("time", "")),
        "station": str(row.get("station", "")),
        "station_code": str(row.get("station_code", "")),
        "observed_event": str(row.get("observed") or row.get("raw_observed_event") or ""),
        "source_file": str(row.get("source_file", "")),
        "source_sheet": str(row.get("source_sheet", "")),
        "raw_json": Json(row),
    }


def migrate_historical_archive(connection, records: list[dict[str, Any]]) -> dict[str, int]:
    if not records:
        return {"historical_observations": 0, "historical_records": 0, "thunderstorm_registry": 0}
    archive_sql = """
    INSERT INTO {table} (
        record_date, observation_time, station, station_code, observed_event,
        source_file, source_sheet, raw_json
    )
    VALUES (
        %(record_date)s, %(observation_time)s, %(station)s, %(station_code)s,
        %(observed_event)s, %(source_file)s, %(source_sheet)s, %(raw_json)s
    )
    """
    registry_sql = """
    INSERT INTO thunderstorm_registry (
        record_date, observation_time, station, station_code, observed_event,
        thunderstorm, nwx, severe_storm, forecast_result, verification_result,
        season, source_dataset
    )
    VALUES (
        %(record_date)s, %(observation_time)s, %(station)s, %(station_code)s,
        %(observed_event)s, %(thunderstorm)s, %(nwx)s, %(severe_storm)s,
        %(forecast_result)s, %(verification_result)s, %(season)s, %(source_dataset)s
    )
    """
    archive_payload = [_history_insert_payload(row) for row in records]
    registry_payload = []
    for row in records:
        observed = str(row.get("observed") or row.get("raw_observed_event") or "")
        registry_payload.append({
            "record_date": _normalize_date(row.get("date")),
            "observation_time": str(row.get("time", "")),
            "station": str(row.get("station", "")),
            "station_code": str(row.get("station_code", "")),
            "observed_event": observed,
            "thunderstorm": bool(row.get("thunderstorm")),
            "nwx": bool(row.get("nwx")),
            "severe_storm": observed.strip().upper() in ("SEVERE TS", "SQ"),
            "forecast_result": None,
            "verification_result": None,
            "season": str(row.get("season", "")),
            "source_dataset": str(row.get("source_file", "")),
        })
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE historical_observations RESTART IDENTITY")
        cursor.execute("TRUNCATE historical_records RESTART IDENTITY")
        cursor.execute("TRUNCATE thunderstorm_registry RESTART IDENTITY")
        cursor.executemany(archive_sql.format(table="historical_observations"), archive_payload)
        cursor.executemany(archive_sql.format(table="historical_records"), archive_payload)
        cursor.executemany(registry_sql, registry_payload)
    connection.commit()
    return {
        "historical_observations": len(archive_payload),
        "historical_records": len(archive_payload),
        "thunderstorm_registry": len(registry_payload),
    }


def migrate_users(connection, records: list[dict[str, Any]]):
    sql = """
    INSERT INTO users (id, name, email, password, role, created_at)
    VALUES (%(id)s, %(name)s, %(email)s, %(password)s, %(role)s, %(created_at)s)
    ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        email = EXCLUDED.email,
        password = EXCLUDED.password,
        role = EXCLUDED.role,
        created_at = EXCLUDED.created_at
    """
    with connection.cursor() as cursor:
        cursor.executemany(sql, records)
        cursor.execute("SELECT setval(pg_get_serial_sequence('users','id'), COALESCE((SELECT MAX(id) FROM users), 1), true)")
    connection.commit()


def migrate_forecasts(connection, records: list[dict[str, Any]]):
    sql = """
    INSERT INTO thunderstorm_forecasts (
        id, station, station_code, cape, lifted_index, sweat_index, k_index, pwat,
        forecast, storm_probability, created_at
    )
    VALUES (
        %(id)s, %(station)s, %(station_code)s, %(cape)s, %(lifted_index)s, %(sweat_index)s,
        %(k_index)s, %(pwat)s, %(forecast)s, %(storm_probability)s, %(created_at)s
    )
    ON CONFLICT (id) DO UPDATE SET
        station = EXCLUDED.station,
        station_code = EXCLUDED.station_code,
        cape = EXCLUDED.cape,
        lifted_index = EXCLUDED.lifted_index,
        sweat_index = EXCLUDED.sweat_index,
        k_index = EXCLUDED.k_index,
        pwat = EXCLUDED.pwat,
        forecast = EXCLUDED.forecast,
        storm_probability = EXCLUDED.storm_probability,
        created_at = EXCLUDED.created_at
    """
    with connection.cursor() as cursor:
        cursor.executemany(sql, records)
        cursor.execute("SELECT setval(pg_get_serial_sequence('thunderstorm_forecasts','id'), COALESCE((SELECT MAX(id) FROM thunderstorm_forecasts), 1), true)")
    connection.commit()


def validate_counts(connection, expected: dict[str, int]) -> dict[str, dict[str, int | bool]]:
    results = {}
    with connection.cursor() as cursor:
        for table, expected_count in expected.items():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            actual = int(cursor.fetchone()[0])
            results[table] = {
                "expected": expected_count,
                "actual": actual,
                "valid": actual >= expected_count,
            }
    return results


def collect_table_counts(connection, tables: list[str]) -> dict[str, int | str]:
    results: dict[str, int | str] = {}
    with connection.cursor() as cursor:
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                results[table] = int(cursor.fetchone()[0])
            except Exception as exc:
                connection.rollback()
                results[table] = f"ERROR: {exc}"
    return results


def collect_connection_audit(connection) -> dict[str, Any]:
    audit: dict[str, Any] = {
        "dotenv_loaded": DOTENV_LOADED,
        "dotenv_path": str(DOTENV_PATH) if DOTENV_PATH else "",
        "database_url_detected": bool(os.getenv("DATABASE_URL", "").strip()),
        "database_url_redacted": _redact_url(os.getenv("DATABASE_URL", "").strip()),
        "supabase_db_host": os.getenv("SUPABASE_DB_HOST", ""),
        "client_ssl_in_use": getattr(getattr(connection, "info", None), "ssl_in_use", None),
    }
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database(), current_user, inet_server_addr()::text, inet_server_port()")
        db_name, db_user, server_addr, server_port = cursor.fetchone()
        audit.update({
            "database": db_name,
            "user": db_user,
            "server_addr": server_addr,
            "server_port": server_port,
        })
        try:
            cursor.execute("SELECT ssl FROM pg_stat_ssl WHERE pid = pg_backend_pid()")
            row = cursor.fetchone()
            audit["ssl_enabled"] = bool(row[0]) if row else False
        except Exception as exc:
            connection.rollback()
            audit["ssl_enabled"] = "UNVERIFIED"
            audit["ssl_check_error"] = str(exc)
    return audit


def collect_integrity_audit(connection) -> dict[str, Any]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT table_name, constraint_type, COUNT(*)
            FROM information_schema.table_constraints
            WHERE table_schema = 'public'
              AND table_name = ANY(%s)
            GROUP BY table_name, constraint_type
            ORDER BY table_name, constraint_type
            """,
            (VALIDATION_TABLES,),
        )
        constraints = [
            {"table": row[0], "type": row[1], "count": int(row[2])}
            for row in cursor.fetchall()
        ]
        cursor.execute(
            """
            SELECT tablename, indexname
            FROM pg_indexes
            WHERE schemaname = 'public'
              AND tablename = ANY(%s)
            ORDER BY tablename, indexname
            """,
            (VALIDATION_TABLES,),
        )
        indexes = [{"table": row[0], "index": row[1]} for row in cursor.fetchall()]
    return {
        "constraints": constraints,
        "indexes": indexes,
        "constraint_count": len(constraints),
        "index_count": len(indexes),
    }


def write_reports(summary: dict[str, Any]):
    connection = summary.get("connection", {})
    records = summary.get("records_imported", {})
    counts = summary.get("table_counts", {})
    validation = summary.get("validation", {})
    integrity = summary.get("integrity", {})

    Path("DATABASE_CONNECTION_AUDIT.md").write_text(
        "\n".join([
            "# Database Connection Audit",
            "",
            f"- Dotenv loaded: {connection.get('dotenv_loaded')}",
            f"- Dotenv path: `{connection.get('dotenv_path')}`",
            f"- DATABASE_URL detected: {connection.get('database_url_detected')}",
            f"- DATABASE_URL: `{connection.get('database_url_redacted')}`",
            f"- SUPABASE_DB_HOST: `{connection.get('supabase_db_host')}`",
            f"- Database: `{connection.get('database')}`",
            f"- User: `{connection.get('user')}`",
            f"- Server: `{connection.get('server_addr')}:{connection.get('server_port')}`",
            f"- Client SSL in use: {connection.get('client_ssl_in_use')}",
            f"- Server-side `pg_stat_ssl` visible as SSL: {connection.get('ssl_enabled')}",
            "",
            "Result: Supabase PostgreSQL connection was validated through the migration runner. Client SSL is the authoritative check for this pooler connection.",
            "",
        ]),
        encoding="utf-8",
    )

    Path("SUPABASE_MIGRATION_REPORT.md").write_text(
        "\n".join([
            "# Supabase Migration Report",
            "",
            f"- Dump directory: `{summary.get('dump_dir')}`",
            f"- Apply mode completed: {summary.get('applied')}",
            f"- Users imported: {records.get('users', 0)}",
            f"- Forecast records imported: {records.get('thunderstorm_forecasts', 0)}",
            f"- Historical observations imported: {records.get('historical_observations', 0)}",
            f"- Historical records imported: {records.get('historical_records', 0)}",
            f"- Thunderstorm registry records imported: {records.get('thunderstorm_registry', 0)}",
            f"- Verification records imported: {records.get('verification_results', 0)}",
            f"- Uploaded datasets imported: {records.get('uploaded_datasets', 0)}",
            f"- Failed imports: {len(summary.get('failed_imports', []))}",
            "",
            "## Source Tables",
            "",
            *[f"- {table}: {count}" for table, count in summary.get("source_tables", {}).items()],
            "",
            "## Optional Tables Not Present In MySQL Export",
            "",
            *[f"- {table}" for table in summary.get("optional_tables_not_present_in_mysql_export", [])],
            "",
        ]),
        encoding="utf-8",
    )

    Path("TABLE_VALIDATION_REPORT.md").write_text(
        "\n".join([
            "# Table Validation Report",
            "",
            "## Row Counts",
            "",
            *[f"- {table}: {count}" for table, count in counts.items()],
            "",
            "## Expected Count Validation",
            "",
            *[
                f"- {table}: expected >= {result.get('expected')}, actual {result.get('actual')}, valid={result.get('valid')}"
                for table, result in validation.items()
            ],
            "",
            "## Integrity Summary",
            "",
            f"- Constraint groups detected: {integrity.get('constraint_count', 0)}",
            f"- Indexes detected: {integrity.get('index_count', 0)}",
            "",
            "## Indexes",
            "",
            *[f"- {idx.get('table')}: `{idx.get('index')}`" for idx in integrity.get("indexes", [])],
            "",
        ]),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description="StormSense AI MySQL dump to Supabase PostgreSQL migration runner")
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR), help="Directory containing MySQL Workbench dump SQL files")
    parser.add_argument("--apply", action="store_true", help="Apply schema and migrate rows into DATABASE_URL")
    parser.add_argument("--summary", default=str(ROOT / "MIGRATION_TEST_REPORT.generated.json"), help="Write JSON migration summary")
    args = parser.parse_args()

    dump_dir = Path(args.dump_dir)
    users = load_table_records(dump_dir, "users")
    forecasts = load_table_records(dump_dir, "thunderstorm_forecasts")
    historical_rows, historical_error = load_historical_rows_for_migration()
    summary: dict[str, Any] = {
        "dump_dir": str(dump_dir),
        "source_tables": {
            "users": len(users),
            "thunderstorm_forecasts": len(forecasts),
            "historical_observations": len(historical_rows),
        },
        "optional_tables_not_present_in_mysql_export": OPTIONAL_TABLES_NOT_IN_EXPORT,
        "applied": False,
        "validation": {},
        "records_imported": {},
        "table_counts": {},
        "failed_imports": [],
    }
    if historical_error:
        summary["failed_imports"].append({"table": "historical_observations", "error": historical_error})

    if args.apply:
        emit_environment_diagnostics()
        connection = connect_to_supabase()
        try:
            summary["connection"] = collect_connection_audit(connection)
            apply_schema(connection)
            migrate_users(connection, users)
            migrate_forecasts(connection, forecasts)
            archive_counts = migrate_historical_archive(connection, historical_rows)
            summary["records_imported"] = {
                "users": len(users),
                "thunderstorm_forecasts": len(forecasts),
                "verification_results": 0,
                "uploaded_datasets": 0,
                **archive_counts,
            }
            summary["validation"] = validate_counts(connection, {
                "users": len(users),
                "thunderstorm_forecasts": len(forecasts),
                "historical_observations": len(historical_rows),
                "historical_records": len(historical_rows),
                "thunderstorm_registry": len(historical_rows),
                "uploaded_datasets": 0,
                "verification_results": 0,
            })
            summary["table_counts"] = collect_table_counts(connection, VALIDATION_TABLES)
            summary["integrity"] = collect_integrity_audit(connection)
            summary["applied"] = True
            write_reports(summary)
        finally:
            connection.close()

    Path(args.summary).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
