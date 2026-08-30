-- ============================================================
-- 09.01 Yellow Taxi Cleaned Layer
-- ============================================================
-- Purpose:
-- Create the cleaned Yellow Taxi dataset from the staging layer.
--
-- Staging data is preserved unchanged.
-- The cleaned layer standardizes naming, creates analytical
-- fields, and flags records requiring further investigation.
-- ============================================================


DROP TABLE IF EXISTS cleaned.yellow_trips_clean;


CREATE TABLE cleaned.yellow_trips_clean AS

SELECT

    -- --------------------------------------------------------
    -- Identifiers
    -- --------------------------------------------------------

    vendorid AS vendor_id,

    -- --------------------------------------------------------
    -- Timestamps
    -- --------------------------------------------------------

    tpep_pickup_datetime AS pickup_datetime,

    tpep_dropoff_datetime AS dropoff_datetime,

    -- --------------------------------------------------------
    -- Derived trip metrics
    -- --------------------------------------------------------

    EXTRACT(
        EPOCH FROM (
            tpep_dropoff_datetime - tpep_pickup_datetime
        )
    ) AS trip_duration_seconds,

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

    -- --------------------------------------------------------
    -- Financial fields
    -- --------------------------------------------------------

    fare_amount,

    extra,

    mta_tax,

    tip_amount,

    tolls_amount,

    improvement_surcharge,

    total_amount,

    congestion_surcharge,

    airport_fee,

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
        WHEN tpep_pickup_datetime >= tpep_dropoff_datetime
        THEN TRUE
        ELSE FALSE
    END AS is_invalid_timestamp

FROM staging.yellow_trips;