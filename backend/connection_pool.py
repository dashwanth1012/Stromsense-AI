from typing import Any

from backend.database import (
    database_configured,
    database_status,
    execute_write,
    fetch_all,
    fetch_one,
    get_engine,
    init_database_schema,
)


SUPABASE_STORAGE_BUCKETS = [
    "historical-archives",
    "uploaded-soundings",
    "forecast-exports",
    "reviewer-dockets",
    "imd-bulletins",
    "research-documents",
]


def get_database_status() -> dict[str, Any]:
    engine = get_engine()
    return {
        "status": database_status(),
        "configured": database_configured(),
        "engine": "postgresql",
        "pool_size": getattr(getattr(engine, "pool", None), "size", lambda: 0)() if engine else 0,
        "storage_buckets": SUPABASE_STORAGE_BUCKETS,
    }


def initialize_supabase_schema() -> bool:
    return init_database_schema()


__all__ = [
    "SUPABASE_STORAGE_BUCKETS",
    "database_configured",
    "execute_write",
    "fetch_all",
    "fetch_one",
    "get_database_status",
    "initialize_supabase_schema",
]
