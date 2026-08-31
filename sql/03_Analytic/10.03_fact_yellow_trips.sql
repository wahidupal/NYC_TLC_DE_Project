-- ============================================================
-- 10.03 Yellow Taxi Trip Fact
-- ============================================================
-- Purpose:
-- Create the Gold fact table for Yellow Taxi trips.
--
-- Grain:
-- One row represents one Yellow Taxi trip.
--
-- Source:
-- cleaned.yellow_trips_clean
--
-- The fact table preserves:
--   - trip timestamps
--   - trip characteristics
--   - location keys
--   - financial measures
--   - data-quality flags
--
-- Location descriptions remain in gold.dim_location.
-- ============================================================


DROP TABLE IF EXISTS gold.fact_yellow_trips;


CREATE TABLE gold.fact_yellow_trips AS

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

    -- --------------------------------------------------------
    -- Trip characteristics
    -- --------------------------------------------------------

    passenger_count,

    rate_code_id,

    store_and_forward_flag,

    payment_type,

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

    improvement_surcharge,

    congestion_surcharge,

    airport_fee,

    cbd_congestion_fee,

    total_amount,

    -- --------------------------------------------------------
    -- Data-quality flags
    -- --------------------------------------------------------

    is_negative_fare,

    is_negative_total,

    is_invalid_timestamp

FROM cleaned.yellow_trips_clean;