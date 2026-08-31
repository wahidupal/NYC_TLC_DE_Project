-- ============================================================
-- 09.03 FHV Cleaned Layer
-- ============================================================
-- Purpose:
-- Create the cleaned FHV dataset from the staging layer.
--
-- Staging data is preserved unchanged.
-- The cleaned layer:
--   1. Standardizes column names
--   2. Removes objectively invalid timestamp records
--   3. Creates analytical trip metrics
--   4. Preserves NULL location IDs
--   5. Adds data-quality flags
-- ============================================================


DROP TABLE IF EXISTS cleaned.fhv_trips_clean;


CREATE TABLE cleaned.fhv_trips_clean AS

SELECT

    -- --------------------------------------------------------
    -- Identifiers
    -- --------------------------------------------------------

    dispatching_base_num AS dispatching_base_number,

    affiliated_base_number AS affiliated_base_number,

    -- --------------------------------------------------------
    -- Timestamps
    -- --------------------------------------------------------

    pickup_datetime,

    dropoff_datetime,

    -- --------------------------------------------------------
    -- Derived trip metrics
    -- --------------------------------------------------------

    EXTRACT(
        EPOCH FROM (
            dropoff_datetime - pickup_datetime
        )
    ) AS trip_duration_seconds,

    -- --------------------------------------------------------
    -- Location information
    -- --------------------------------------------------------

    pulocationid AS pickup_location_id,

    dolocationid AS dropoff_location_id,

    -- --------------------------------------------------------
    -- Shared ride flag
    -- --------------------------------------------------------

    sr_flag,

    -- --------------------------------------------------------
    -- Data-quality flags
    -- --------------------------------------------------------

    CASE
        WHEN pickup_datetime > dropoff_datetime
        THEN TRUE
        ELSE FALSE
    END AS is_invalid_timestamp,

    CASE
        WHEN pulocationid IS NULL
          OR dolocationid IS NULL
        THEN TRUE
        ELSE FALSE
    END AS has_missing_location

FROM staging.fhv_trips

-- ------------------------------------------------------------
-- Remove objectively invalid timestamp records
-- ------------------------------------------------------------

WHERE pickup_datetime <= dropoff_datetime;