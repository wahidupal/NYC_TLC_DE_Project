-- ============================================================
-- 10.04 Green Taxi Trip Fact
-- ============================================================
-- Purpose:
-- Create the Gold fact table for Green Taxi trips.
--
-- Grain:
-- One row represents one Green Taxi trip.
--
-- Source:
-- cleaned.green_trips_clean
--
-- Location descriptions remain in gold.dim_location.
-- Location IDs are retained as foreign-key-style references.
-- ============================================================


DROP TABLE IF EXISTS gold.fact_green_trips;


CREATE TABLE gold.fact_green_trips AS

SELECT

    -- --------------------------------------------------------
    -- Identifiers
    -- --------------------------------------------------------

    vendor_id,

    -- --------------------------------------------------------
    -- Trip timestamps
    -- --------------------------------------------------------

    pickup_datetime,

    dropoff_datetime,

    -- --------------------------------------------------------
    -- Derived trip metrics
    -- --------------------------------------------------------

    trip_duration_seconds,

    trip_distance_miles,

    is_zero_duration,

    -- --------------------------------------------------------
    -- Trip characteristics
    -- --------------------------------------------------------

    passenger_count,

    rate_code_id,

    store_and_forward_flag,

    payment_type,

    trip_type,

    -- --------------------------------------------------------
    -- Location keys
    -- --------------------------------------------------------

    pickup_location_id,

    dropoff_location_id,

    -- --------------------------------------------------------
    -- Financial measures
    -- --------------------------------------------------------

    fare_amount,

    extra,

    mta_tax,

    tip_amount,

    tolls_amount,

    ehail_fee,

    improvement_surcharge,

    congestion_surcharge,

    cbd_congestion_fee,

    total_amount,

    -- --------------------------------------------------------
    -- Data-quality flags
    -- --------------------------------------------------------

    is_negative_fare,

    is_negative_total,

    is_invalid_timestamp

FROM cleaned.green_trips_clean;