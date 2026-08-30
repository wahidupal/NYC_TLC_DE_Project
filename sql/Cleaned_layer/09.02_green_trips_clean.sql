-- ============================================================
-- 09.02 Green Taxi Cleaned Layer
-- ============================================================
-- Purpose:
-- Create the cleaned Green Taxi dataset from the staging layer.
--
-- Staging data is preserved unchanged.
-- The cleaned layer:
--   1. Standardizes column names
--   2. Removes records with objectively invalid timestamp ordering
--   3. Creates analytical trip metrics
--   4. Preserves suspicious financial values
--   5. Adds data-quality flags for further investigation
-- ============================================================


DROP TABLE IF EXISTS cleaned.green_trips_clean;


CREATE TABLE cleaned.green_trips_clean AS

SELECT

    -- --------------------------------------------------------
    -- Identifiers
    -- --------------------------------------------------------

    vendorid AS vendor_id,

    -- --------------------------------------------------------
    -- Timestamps
    -- --------------------------------------------------------

    lpep_pickup_datetime AS pickup_datetime,

    lpep_dropoff_datetime AS dropoff_datetime,

    -- --------------------------------------------------------
    -- Derived trip metrics
    -- --------------------------------------------------------

    EXTRACT(
        EPOCH FROM (
            lpep_dropoff_datetime - lpep_pickup_datetime
        )
    ) AS trip_duration_seconds,

    CASE
        WHEN lpep_pickup_datetime = lpep_dropoff_datetime
        THEN TRUE
        ELSE FALSE
    END AS is_zero_duration,

    -- --------------------------------------------------------
    -- Trip characteristics
    -- --------------------------------------------------------

    passenger_count,

    trip_distance AS trip_distance_miles,

    ratecodeid AS rate_code_id,

    store_and_fwd_flag AS store_and_forward_flag,

    pulocationid AS pickup_location_id,

    dolocationid AS dropoff_location_id,

    payment_type,

    trip_type,

    -- --------------------------------------------------------
    -- Financial fields
    -- --------------------------------------------------------

    fare_amount,

    extra,

    mta_tax,

    tip_amount,

    tolls_amount,

    ehail_fee,

    improvement_surcharge,

    total_amount,

    congestion_surcharge,

    cbd_congestion_fee,

    -- --------------------------------------------------------
    -- Data-quality flags
    -- --------------------------------------------------------

    CASE
        WHEN fare_amount < 0
        THEN TRUE
        ELSE FALSE
    END AS is_negative_fare,

    CASE
        WHEN total_amount < 0
        THEN TRUE
        ELSE FALSE
    END AS is_negative_total,

    CASE
        WHEN lpep_pickup_datetime > lpep_dropoff_datetime
        THEN TRUE
        ELSE FALSE
    END AS is_invalid_timestamp

FROM staging.green_trips

-- ------------------------------------------------------------
-- Remove objectively invalid timestamp records
-- ------------------------------------------------------------

WHERE lpep_pickup_datetime <= lpep_dropoff_datetime;