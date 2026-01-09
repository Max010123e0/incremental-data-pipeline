# Bronze Layer — Raw Ingestion

The Bronze layer stores **raw data ingested from four heterogeneous sources** with minimal transformation.  
Each source is modeled independently to preserve original structure and ingestion semantics.

### Source 1 — Hourly CSV Files
Simulates file-based ingestion where upstream systems drop hourly CSV event files. Data is ingested as-is into Snowflake using staged file loads.

### Source 2 — API Source (Batch / Streaming-style)
Simulates an external API that returns new or updated events based on a timestamp. Designed to handle incremental loads and late-arriving data.

### Source 3 — On-Prem SQL Server (DB A)
Simulates an operational database generating new records every ~10 minutes. Data is ingested incrementally using an `updated_at`.

### Source 4 — On-Prem SQL Server (DB B)
Simulates a second operational database with a different schema and update pattern. Ingested independently to reflect heterogeneous upstream systems.