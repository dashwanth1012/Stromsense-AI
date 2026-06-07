from connection_pool import fetch_all, fetch_one, get_database_status


def health_check():
    return get_database_status()


__all__ = ["fetch_all", "fetch_one", "health_check"]
