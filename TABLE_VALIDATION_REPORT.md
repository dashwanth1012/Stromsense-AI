# Table Validation Report

## Public Migration Tables

- Total tables present: 12
- Tables: `audit_login`, `audit_logs`, `historical_observations`, `historical_records`, `profiles`, `reviewer_dashboard_records`, `roles`, `thunderstorm_forecasts`, `thunderstorm_registry`, `uploaded_datasets`, `users`, `verification_results`

## Row Counts

- users: 3
- thunderstorm_forecasts: 947
- historical_observations: 360
- historical_records: 360
- thunderstorm_registry: 360
- uploaded_datasets: 0
- verification_results: 0
- reviewer_dashboard_records: 0

## Expected Count Validation

- users: expected >= 3, actual 3, valid=True
- thunderstorm_forecasts: expected >= 942, actual 947, valid=True
- historical_observations: expected >= 360, actual 360, valid=True
- historical_records: expected >= 360, actual 360, valid=True
- thunderstorm_registry: expected >= 360, actual 360, valid=True
- uploaded_datasets: expected >= 0, actual 0, valid=True
- verification_results: expected >= 0, actual 0, valid=True

## Integrity Summary

- Constraint groups detected: 17
- Indexes detected: 15

## `thunderstorm_forecasts` Schema Verification

- id: bigint
- station: character varying
- station_code: character varying
- cape: double precision
- lifted_index: double precision
- sweat_index: double precision
- k_index: double precision
- pwat: double precision
- forecast: character varying
- storm_probability: integer
- created_at: timestamp without time zone

Result: Supabase table `thunderstorm_forecasts` is present and accepts migrated Workbench forecast rows plus live forecast-history writes.

## Indexes

- historical_observations: `historical_observations_pkey`
- historical_observations: `idx_historical_observations_station_date`
- historical_records: `historical_records_pkey`
- historical_records: `idx_historical_records_station_date`
- reviewer_dashboard_records: `reviewer_dashboard_records_pkey`
- thunderstorm_forecasts: `idx_thunderstorm_forecasts_created_at`
- thunderstorm_forecasts: `idx_thunderstorm_forecasts_station_created_at`
- thunderstorm_forecasts: `thunderstorm_forecasts_pkey`
- thunderstorm_registry: `idx_thunderstorm_registry_event_flags`
- thunderstorm_registry: `idx_thunderstorm_registry_station_date`
- thunderstorm_registry: `thunderstorm_registry_pkey`
- uploaded_datasets: `uploaded_datasets_pkey`
- users: `users_email_key`
- users: `users_pkey`
- verification_results: `verification_results_pkey`
