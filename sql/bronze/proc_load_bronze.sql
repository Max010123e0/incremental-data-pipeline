USE ROLE ACCOUNTADMIN;
USE WAREHOUSE PIPELINE_WH;
USE DATABASE PIPELINE_DB;
USE SCHEMA BRONZE;

-- ============================================================
-- Bronze Load Runner 
-- Runs full reloads into Bronze tables for each source
-- ============================================================

-- ---------------------------
-- Source 1: Hourly CSV -> RAW_CSV_EVENTS
-- Assumes files are already present in @CSV_EVENTS_STAGE
-- ---------------------------
TRUNCATE TABLE RAW_CSV_EVENTS;

COPY INTO RAW_CSV_EVENTS
FROM @CSV_EVENTS_STAGE
ON_ERROR = 'ABORT_STATEMENT';

-- Source 2: API -> RAW_API_EVENTS
TRUNCATE TABLE RAW_API_EVENTS;

COPY INTO RAW_API_EVENTS (payload)
FROM @API_EVENTS_STAGE
ON_ERROR = 'ABORT_STATEMENT';

UPDATE RAW_API_EVENTS
SET ingestion_ts = COALESCE(ingestion_ts, CURRENT_TIMESTAMP()),
    source_since = COALESCE(source_since, TO_TIMESTAMP_NTZ('2026-01-05T15:00:00'));
-- Source 3: SQLServer_A 
-- Source 4: SQLServer_B 