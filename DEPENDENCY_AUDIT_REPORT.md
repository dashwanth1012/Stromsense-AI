# StormSense AI Render Dependency Audit Report

Generated: 2026-06-08

## Scope

Deployment recovery was limited to Python dependency and startup readiness for the existing backend package.

- Backend source scanned: `backend/**/*.py`
- Excluded from source audit: `backend/venv/**`, `__pycache__`
- Requirements file updated: `backend/requirements.txt`
- No forecasting, CAPE, probability, verification, database logic, archive logic, or frontend code was modified.

## Files Scanned

| File | Status |
|---|---|
| `backend/analysis_engines.py` | Scanned |
| `backend/connection_pool.py` | Scanned |
| `backend/database.py` | Scanned |
| `backend/db.py` | Scanned |
| `backend/fetch_sounding.py` | Scanned |
| `backend/json_forecast.py` | Scanned |
| `backend/main.py` | Scanned |
| `backend/multi_station_predictor.py` | Scanned |
| `backend/rsrw_archive.py` | Scanned |
| `backend/storm_predictor.py` | Scanned |
| `backend/thermo.py` | Scanned |
| `backend/threshold_engine.py` | Scanned |
| `backend/__init__.py` | Scanned |
| `backend/ml/train_model.py` | Scanned |

## Dependency Matrix

| Imported Module / Runtime Need | Requirement Package | Found Before | Action Taken | Validation Result |
|---|---|---:|---|---|
| `fastapi` | `fastapi` | Yes | Kept | Import OK |
| `uvicorn` startup | `uvicorn` | Yes | Kept | `uvicorn backend.main:app --host 0.0.0.0 --port 8000` started OK |
| `pandas` | `pandas` | Yes | Kept | Import OK |
| `numpy` | `numpy` | Yes | Kept | Satisfied through existing analytics stack |
| `requests` | `requests` | Yes | Kept | Import OK |
| `bs4` | `beautifulsoup4` | Yes | Kept | Import OK |
| `dotenv` | `python-dotenv` | Yes | Kept | Import OK |
| `sqlalchemy` | `SQLAlchemy` | Yes | Kept | Import OK |
| PostgreSQL driver | `psycopg2-binary` | Yes | Kept | `backend.main` DB initialization OK |
| `pydantic` | `pydantic` | Yes | Kept | Import OK |
| `joblib` | `joblib` | Yes | Kept | Import OK |
| `sklearn` | `scikit-learn` | No | Added `scikit-learn>=1.5,<2.0` | Import OK |
| `.xlsx` read/write via pandas | `openpyxl` | No | Added `openpyxl>=3.1,<4.0` | Import OK |
| legacy `.xls` read via pandas | `xlrd` | No | Added `xlrd>=2.0,<3.0`; installed locally for validation | Import OK |
| FastAPI upload parsing | `python-multipart` | Yes | Kept | Existing upload dependency preserved |
| websocket support | `websockets`, `wsproto` | Yes | Kept | Existing websocket dependencies preserved |
| Supabase compatibility | `supabase` | Yes | Kept | Existing Supabase dependency preserved |

## Incorrect / Obsolete / Duplicate Entry Review

- No `sklearn` package entry exists in `backend/requirements.txt`; the correct package name `scikit-learn` is now present.
- No duplicate package names were found in `backend/requirements.txt`.
- Existing valid packages were preserved.
- No additional requirements files were created.

## Validation Commands

| Validation | Result |
|---|---|
| `python -c "import fastapi, pandas, requests, bs4, dotenv, sqlalchemy, pydantic, joblib, sklearn, openpyxl, xlrd; print('FULL_DEPENDENCY_IMPORT_OK')"` | Passed |
| `python -c "import backend.main"` | Passed |
| `python -c "import backend.main; print('IMPORT_OK')"` | Passed |
| `uvicorn backend.main:app --host 0.0.0.0 --port 8000` | Started successfully; application startup complete |
| `python -m pip check` | Passed: no broken requirements |

## Deployment Readiness Conclusion

Render dependency recovery is complete. The backend package imports successfully, the Render-style Uvicorn target starts without `ModuleNotFoundError` or `ImportError`, and the existing `backend/requirements.txt` now includes the missing deployment dependencies needed by the backend import graph and Excel dataset workflows.
