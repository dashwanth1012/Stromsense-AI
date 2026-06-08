# StormSense AI API Reference

Generated from `backend/main.py` on 2026-06-08.

Total API/websocket route decorators discovered: 54.

| Method | Route | Handler | Purpose | Source |
| --- | --- | --- | --- | --- |
| POST | /auth/signup | signup | Register an operational user in the StormSense authentication store. | backend/main.py:575 |
| POST | /auth/login | login | Authenticate a reviewer/operator and return a bearer token plus user profile. | backend/main.py:613 |
| GET | /auth/me | auth_me | Return the authenticated operator profile for session validation. | backend/main.py:703 |
| POST | /cwc/override | trigger_override | Expose trigger override workflow output for the operational workstation. | backend/main.py:711 |
| POST | /cwc/clear-override | clear_override | Expose clear override workflow output for the operational workstation. | backend/main.py:732 |
| POST | /cwc/cycle | update_cycle | Expose update cycle workflow output for the operational workstation. | backend/main.py:754 |
| GET | /cwc/cycle | get_cycle | Expose get cycle workflow output for the operational workstation. | backend/main.py:765 |
| GET | / | home | Expose home workflow output for the operational workstation. | backend/main.py:1558 |
| GET | /forecast | forecast | Generate live station forecasts using sounding, thermodynamic, probability, and decision-support engines. | backend/main.py:1574 |
| GET | /history | history | Return recent persisted thunderstorm forecast records. | backend/main.py:1592 |
| GET | /trend-analysis | trend_analysis | Return station-level trend analysis for convective evolution monitoring. | backend/main.py:1636 |
| GET | /storm-escalation | storm_escalation | Return severe escalation records for high-risk station monitoring. | backend/main.py:1670 |
| WEBSOCKET | /stream/atmospheric | stream_atmospheric | Stream atmospheric forecast, trend, escalation, and cycle metadata over websocket. | backend/main.py:1717 |
| GET | /system-status | system_status | Return backend, database, websocket, and runtime health status. | backend/main.py:1769 |
| GET | /cwc/correlation | get_cwc_correlation | Expose get cwc correlation workflow output for the operational workstation. | backend/main.py:1792 |
| GET | /cwc/optimization | get_cwc_optimization | Expose get cwc optimization workflow output for the operational workstation. | backend/main.py:1796 |
| GET | /cwc/verification | get_cwc_verification | Expose get cwc verification workflow output for the operational workstation. | backend/main.py:1800 |
| GET | /cwc/thresholds | get_cwc_thresholds | Expose get cwc thresholds workflow output for the operational workstation. | backend/main.py:1804 |
| GET | /cwc/index-catalog | get_cwc_index_catalog | Expose get cwc index catalog workflow output for the operational workstation. | backend/main.py:1817 |
| GET | /cwc/seasonal-analysis | get_cwc_seasonal_analysis | Expose get cwc seasonal analysis workflow output for the operational workstation. | backend/main.py:1821 |
| GET | /cwc/replay-cases | get_cwc_replay_cases | Expose get cwc replay cases workflow output for the operational workstation. | backend/main.py:1825 |
| GET | /cwc/observations | get_cwc_observations | Expose get cwc observations workflow output for the operational workstation. | backend/main.py:1829 |
| GET | /cwc/observational-analytics | get_cwc_observational_analytics | Expose get cwc observational analytics workflow output for the operational workstation. | backend/main.py:1833 |
| GET | /cwc/probabilistic-forecast | get_cwc_probabilistic_forecast | Expose get cwc probabilistic forecast workflow output for the operational workstation. | backend/main.py:1837 |
| GET | /cwc/thermo-diagnostics | get_cwc_thermo_diagnostics | Expose get cwc thermo diagnostics workflow output for the operational workstation. | backend/main.py:1845 |
| GET | /cwc/verification-advanced | get_cwc_verification_advanced | Expose get cwc verification advanced workflow output for the operational workstation. | backend/main.py:1901 |
| GET | /cwc/ml-ready-dataset | get_cwc_ml_ready_dataset | Expose get cwc ml ready dataset workflow output for the operational workstation. | backend/main.py:1905 |
| GET | /cwc/climatology | get_cwc_climatology | Expose get cwc climatology workflow output for the operational workstation. | backend/main.py:1909 |
| GET | /cwc/decision-support | get_cwc_decision_support | Expose get cwc decision support workflow output for the operational workstation. | backend/main.py:1913 |
| GET | /cwc/operational-bulletins | get_cwc_operational_bulletins | Generate operational bulletin products from current forecast rows. | backend/main.py:1967 |
| GET | /cwc/radar-sounding-fusion | get_cwc_radar_sounding_fusion | Expose get cwc radar sounding fusion workflow output for the operational workstation. | backend/main.py:1974 |
| GET | /cwc/ai-forecast-intelligence | get_cwc_ai_forecast_intelligence | Expose get cwc ai forecast intelligence workflow output for the operational workstation. | backend/main.py:1993 |
| GET | /cwc/coastal-andhra-intelligence | get_cwc_coastal_andhra_intelligence | Expose get cwc coastal andhra intelligence workflow output for the operational workstation. | backend/main.py:2018 |
| GET | /cwc/verification-rolling | get_cwc_verification_rolling | Expose get cwc verification rolling workflow output for the operational workstation. | backend/main.py:2042 |
| GET | /cwc/historical-observations | get_cwc_historical_observations | Expose get cwc historical observations workflow output for the operational workstation. | backend/main.py:2046 |
| GET | /cwc/export/csv | export_cwc_csv | Expose export cwc csv workflow output for the operational workstation. | backend/main.py:2050 |
| GET | /cwc/export/json | export_cwc_json | Expose export cwc json workflow output for the operational workstation. | backend/main.py:2059 |
| GET | /cwc/ml-pipeline | get_cwc_ml_pipeline | Expose get cwc ml pipeline workflow output for the operational workstation. | backend/main.py:2063 |
| GET | /cwc/sounding-raw/{station_code} | get_cwc_sounding_raw | Expose get cwc sounding raw workflow output for the operational workstation. | backend/main.py:2068 |
| GET | /cwc/threshold-research | get_cwc_threshold_research | Expose get cwc threshold research workflow output for the operational workstation. | backend/main.py:2090 |
| GET | /cwc/cape-traceability | get_cwc_cape_traceability | Return station CAPE traceability timeline and static-data warnings. | backend/main.py:2131 |
| GET | /cwc/analog | get_cwc_analog | Expose get cwc analog workflow output for the operational workstation. | backend/main.py:2176 |
| GET | /cwc/forecast-evolution | get_cwc_forecast_evolution | Expose get cwc forecast evolution workflow output for the operational workstation. | backend/main.py:2193 |
| GET | /cwc/district-impact | get_cwc_district_impact | Return district impact intelligence for coastal Andhra monitoring. | backend/main.py:2203 |
| GET | /cwc/historical-files | get_cwc_historical_files | Expose get cwc historical files workflow output for the operational workstation. | backend/main.py:2243 |
| GET | /cwc/historical-dates | get_cwc_historical_dates | Return the historical archive index used by search, registry, and reviewer workflows. | backend/main.py:2440 |
| GET | /cwc/historical-analysis | get_cwc_historical_analysis | Return a full historical case analysis with forecast reproduction and verification fields. | backend/main.py:2489 |
| POST | /cwc/upload-sounding | upload_sounding | Expose upload sounding workflow output for the operational workstation. | backend/main.py:2802 |
| POST | /cwc/analyze-historical-dataset | analyze_historical_dataset | Analyze uploaded CSV/XLS/XLSX historical datasets and build file-based registry output. | backend/main.py:2859 |
| GET | /cwc/latest-file-analyzed | get_latest_file_analyzed | Return the latest uploaded file analysis metadata for dashboard reference. | backend/main.py:3082 |
| POST | /cwc/custom-sounding-analysis | custom_sounding_analysis | Expose custom sounding analysis workflow output for the operational workstation. | backend/main.py:3086 |
| POST | /cwc/research-verification | post_cwc_research_verification | Expose post cwc research verification workflow output for the operational workstation. | backend/main.py:3167 |
| GET | /cwc/export/analysis | export_cwc_analysis | Expose export cwc analysis workflow output for the operational workstation. | backend/main.py:3184 |
| GET | /{full_path:path} | serve_frontend_spa | Expose serve frontend spa workflow output for the operational workstation. | backend/main.py:3265 |

## Endpoint Notes
### POST /auth/signup
Purpose: Register an operational user in the StormSense authentication store.
Handler: `signup` at `backend/main.py:575`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### POST /auth/login
Purpose: Authenticate a reviewer/operator and return a bearer token plus user profile.
Handler: `login` at `backend/main.py:613`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /auth/me
Purpose: Return the authenticated operator profile for session validation.
Handler: `auth_me` at `backend/main.py:703`.
Authentication: Bearer token required.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### POST /cwc/override
Purpose: Expose trigger override workflow output for the operational workstation.
Handler: `trigger_override` at `backend/main.py:711`.
Authentication: Bearer token required.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### POST /cwc/clear-override
Purpose: Expose clear override workflow output for the operational workstation.
Handler: `clear_override` at `backend/main.py:732`.
Authentication: Bearer token required.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### POST /cwc/cycle
Purpose: Expose update cycle workflow output for the operational workstation.
Handler: `update_cycle` at `backend/main.py:754`.
Authentication: Bearer token required.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/cycle
Purpose: Expose get cycle workflow output for the operational workstation.
Handler: `get_cycle` at `backend/main.py:765`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /
Purpose: Expose home workflow output for the operational workstation.
Handler: `home` at `backend/main.py:1558`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /forecast
Purpose: Generate live station forecasts using sounding, thermodynamic, probability, and decision-support engines.
Handler: `forecast` at `backend/main.py:1574`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /history
Purpose: Return recent persisted thunderstorm forecast records.
Handler: `history` at `backend/main.py:1592`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /trend-analysis
Purpose: Return station-level trend analysis for convective evolution monitoring.
Handler: `trend_analysis` at `backend/main.py:1636`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /storm-escalation
Purpose: Return severe escalation records for high-risk station monitoring.
Handler: `storm_escalation` at `backend/main.py:1670`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### WEBSOCKET /stream/atmospheric
Purpose: Stream atmospheric forecast, trend, escalation, and cycle metadata over websocket.
Handler: `stream_atmospheric` at `backend/main.py:1717`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /system-status
Purpose: Return backend, database, websocket, and runtime health status.
Handler: `system_status` at `backend/main.py:1769`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/correlation
Purpose: Expose get cwc correlation workflow output for the operational workstation.
Handler: `get_cwc_correlation` at `backend/main.py:1792`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/optimization
Purpose: Expose get cwc optimization workflow output for the operational workstation.
Handler: `get_cwc_optimization` at `backend/main.py:1796`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/verification
Purpose: Expose get cwc verification workflow output for the operational workstation.
Handler: `get_cwc_verification` at `backend/main.py:1800`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/thresholds
Purpose: Expose get cwc thresholds workflow output for the operational workstation.
Handler: `get_cwc_thresholds` at `backend/main.py:1804`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/index-catalog
Purpose: Expose get cwc index catalog workflow output for the operational workstation.
Handler: `get_cwc_index_catalog` at `backend/main.py:1817`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/seasonal-analysis
Purpose: Expose get cwc seasonal analysis workflow output for the operational workstation.
Handler: `get_cwc_seasonal_analysis` at `backend/main.py:1821`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/replay-cases
Purpose: Expose get cwc replay cases workflow output for the operational workstation.
Handler: `get_cwc_replay_cases` at `backend/main.py:1825`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/observations
Purpose: Expose get cwc observations workflow output for the operational workstation.
Handler: `get_cwc_observations` at `backend/main.py:1829`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/observational-analytics
Purpose: Expose get cwc observational analytics workflow output for the operational workstation.
Handler: `get_cwc_observational_analytics` at `backend/main.py:1833`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/probabilistic-forecast
Purpose: Expose get cwc probabilistic forecast workflow output for the operational workstation.
Handler: `get_cwc_probabilistic_forecast` at `backend/main.py:1837`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/thermo-diagnostics
Purpose: Expose get cwc thermo diagnostics workflow output for the operational workstation.
Handler: `get_cwc_thermo_diagnostics` at `backend/main.py:1845`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/verification-advanced
Purpose: Expose get cwc verification advanced workflow output for the operational workstation.
Handler: `get_cwc_verification_advanced` at `backend/main.py:1901`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/ml-ready-dataset
Purpose: Expose get cwc ml ready dataset workflow output for the operational workstation.
Handler: `get_cwc_ml_ready_dataset` at `backend/main.py:1905`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/climatology
Purpose: Expose get cwc climatology workflow output for the operational workstation.
Handler: `get_cwc_climatology` at `backend/main.py:1909`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/decision-support
Purpose: Expose get cwc decision support workflow output for the operational workstation.
Handler: `get_cwc_decision_support` at `backend/main.py:1913`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/operational-bulletins
Purpose: Generate operational bulletin products from current forecast rows.
Handler: `get_cwc_operational_bulletins` at `backend/main.py:1967`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/radar-sounding-fusion
Purpose: Expose get cwc radar sounding fusion workflow output for the operational workstation.
Handler: `get_cwc_radar_sounding_fusion` at `backend/main.py:1974`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/ai-forecast-intelligence
Purpose: Expose get cwc ai forecast intelligence workflow output for the operational workstation.
Handler: `get_cwc_ai_forecast_intelligence` at `backend/main.py:1993`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/coastal-andhra-intelligence
Purpose: Expose get cwc coastal andhra intelligence workflow output for the operational workstation.
Handler: `get_cwc_coastal_andhra_intelligence` at `backend/main.py:2018`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/verification-rolling
Purpose: Expose get cwc verification rolling workflow output for the operational workstation.
Handler: `get_cwc_verification_rolling` at `backend/main.py:2042`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/historical-observations
Purpose: Expose get cwc historical observations workflow output for the operational workstation.
Handler: `get_cwc_historical_observations` at `backend/main.py:2046`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/export/csv
Purpose: Expose export cwc csv workflow output for the operational workstation.
Handler: `export_cwc_csv` at `backend/main.py:2050`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/export/json
Purpose: Expose export cwc json workflow output for the operational workstation.
Handler: `export_cwc_json` at `backend/main.py:2059`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/ml-pipeline
Purpose: Expose get cwc ml pipeline workflow output for the operational workstation.
Handler: `get_cwc_ml_pipeline` at `backend/main.py:2063`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/sounding-raw/{station_code}
Purpose: Expose get cwc sounding raw workflow output for the operational workstation.
Handler: `get_cwc_sounding_raw` at `backend/main.py:2068`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/threshold-research
Purpose: Expose get cwc threshold research workflow output for the operational workstation.
Handler: `get_cwc_threshold_research` at `backend/main.py:2090`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/cape-traceability
Purpose: Return station CAPE traceability timeline and static-data warnings.
Handler: `get_cwc_cape_traceability` at `backend/main.py:2131`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/analog
Purpose: Expose get cwc analog workflow output for the operational workstation.
Handler: `get_cwc_analog` at `backend/main.py:2176`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/forecast-evolution
Purpose: Expose get cwc forecast evolution workflow output for the operational workstation.
Handler: `get_cwc_forecast_evolution` at `backend/main.py:2193`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/district-impact
Purpose: Return district impact intelligence for coastal Andhra monitoring.
Handler: `get_cwc_district_impact` at `backend/main.py:2203`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/historical-files
Purpose: Expose get cwc historical files workflow output for the operational workstation.
Handler: `get_cwc_historical_files` at `backend/main.py:2243`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/historical-dates
Purpose: Return the historical archive index used by search, registry, and reviewer workflows.
Handler: `get_cwc_historical_dates` at `backend/main.py:2440`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/historical-analysis
Purpose: Return a full historical case analysis with forecast reproduction and verification fields.
Handler: `get_cwc_historical_analysis` at `backend/main.py:2489`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### POST /cwc/upload-sounding
Purpose: Expose upload sounding workflow output for the operational workstation.
Handler: `upload_sounding` at `backend/main.py:2802`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### POST /cwc/analyze-historical-dataset
Purpose: Analyze uploaded CSV/XLS/XLSX historical datasets and build file-based registry output.
Handler: `analyze_historical_dataset` at `backend/main.py:2859`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/latest-file-analyzed
Purpose: Return the latest uploaded file analysis metadata for dashboard reference.
Handler: `get_latest_file_analyzed` at `backend/main.py:3082`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### POST /cwc/custom-sounding-analysis
Purpose: Expose custom sounding analysis workflow output for the operational workstation.
Handler: `custom_sounding_analysis` at `backend/main.py:3086`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### POST /cwc/research-verification
Purpose: Expose post cwc research verification workflow output for the operational workstation.
Handler: `post_cwc_research_verification` at `backend/main.py:3167`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

### GET /cwc/export/analysis
Purpose: Expose export cwc analysis workflow output for the operational workstation.
Handler: `export_cwc_analysis` at `backend/main.py:3184`.
Authentication: Public operational API or UI-facing endpoint.
Input: query parameters, JSON body, uploaded file, or websocket frame according to the route definition.
Output: JSON operational payload unless the route is a websocket, CSV export, raw sounding, or SPA static response.
Error handling: FastAPI status responses, route-specific validation, and fallback cache behavior where implemented.

