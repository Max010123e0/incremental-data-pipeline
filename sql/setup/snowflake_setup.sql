-- ============================================================
-- Project: Incremental Data Pipeline
-- File:    snowflake_setup.sql
-- Purpose: Create a cost-controlled dev warehouse + project DB/schemas
-- ============================================================

-- 1) Role
USE ROLE ACCOUNTADMIN;

-- 2) Warehouse
CREATE WAREHOUSE IF NOT EXISTS PIPELINE_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

USE WAREHOUSE PIPELINE_WH;

-- 3) Database + schemas
CREATE DATABASE IF NOT EXISTS PIPELINE_DB;

CREATE SCHEMA IF NOT EXISTS PIPELINE_DB.BRONZE;
CREATE SCHEMA IF NOT EXISTS PIPELINE_DB.SILVER;
CREATE SCHEMA IF NOT EXISTS PIPELINE_DB.GOLD;
CREATE SCHEMA IF NOT EXISTS PIPELINE_DB.META;

-- 4) Metadata table for tracking pipeline runs / baseline vs improvements
CREATE TABLE IF NOT EXISTS PIPELINE_DB.META.PIPELINE_RUNS (
  run_id STRING,
  run_ts TIMESTAMP_NTZ,
  pipeline_version STRING,   -- either baseline or incremental
  source_name STRING,        
  duration_seconds NUMBER,
  status STRING,          
  notes STRING
);

-- 5) Sanity checks
SELECT CURRENT_ROLE()     AS role,
       CURRENT_WAREHOUSE() AS warehouse;

SHOW SCHEMAS IN DATABASE PIPELINE_DB;

-- 6) Cost control: suspend compute when finished
ALTER WAREHOUSE PIPELINE_WH SUSPEND;
SHOW WAREHOUSES LIKE 'PIPELINE_WH';