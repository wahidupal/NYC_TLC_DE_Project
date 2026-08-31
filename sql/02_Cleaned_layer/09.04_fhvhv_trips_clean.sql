-- ============================================================
-- 09.04 FHVHV Cleaned Layer
-- ============================================================
-- Purpose:
-- Create the cleaned FHVHV dataset from the staging layer.
--
-- Staging data is preserved unchanged.
-- The cleaned layer:
--   1. Standardizes column names
--   2. Creates analytical trip-duration metrics
--   3. Preserves unusual timestamp sequences
--   4. Adds data-quality flags for timestamp issues
--   5. Preserves suspicious financial values
-- ============================================================


DROP TABLE IF EXISTS cleaned.fhvhv_trips_clean;


CREATE TABLE cleaned.fhvhv_trips_clean AS

SELECT

    -- --------------------------------------------------------
    -- Identifiers
    -- --------------------------------------------------------

    hvfhs_license_num AS hvfhv_license_number,

    dispatching_base_num AS dispatching_base_number,

    originating_base_num AS originating_base_number,

    -- --------------------------------------------------------
    -- Operational timestamps
    -- --------------------------------------------------------

    request_datetime,

    on_scene_datetime,

    pickup_datetime,

    dropoff_datetime,

    -- --------------------------------------------------------
    -- Derived time metrics
    -- --------------------------------------------------------

    EXTRACT(
        EPOCH FROM (
            on_scene_datetime - request_datetime
        )
    ) AS request_to_on_scene_seconds,

    EXTRACT(
        EPOCH FROM (
            pickup_datetime - on_scene_datetime
        )
    ) AS on_scene_to_pickup_seconds,

    EXTRACT(
        EPOCH FROM (
            dropoff_datetime - pickup_datetime
        )
    ) AS trip_duration_seconds,

    -- --------------------------------------------------------
    -- Trip characteristics
    -- --------------------------------------------------------

    pulocationid AS pickup_location_id,

    dolocationid AS dropoff_location_id,

    trip_miles,

    trip_time,

    -- --------------------------------------------------------
    -- Financial fields
    -- --------------------------------------------------------

    base_passenger_fare,

    tolls,

    bcf,

    sales_tax,

    congestion_surcharge,

    airport_fee,

    tips,

    driver_pay,

    cbd_congestion_fee,

    -- --------------------------------------------------------
    -- Service / accessibility flags
    -- --------------------------------------------------------

    shared_request_flag,

    shared_match_flag,

    access_a_ride_flag,

    wav_request_flag,

    wav_match_flag,

    -- --------------------------------------------------------
    -- Data-quality flags
    -- --------------------------------------------------------

    CASE
        WHEN request_datetime > on_scene_datetime
        THEN TRUE
        ELSE FALSE
    END AS is_invalid_request_sequence,

    CASE
        WHEN on_scene_datetime > pickup_datetime
        THEN TRUE
        ELSE FALSE
    END AS is_invalid_on_scene_sequence,

    CASE
        WHEN pickup_datetime > dropoff_datetime
        THEN TRUE
        ELSE FALSE
    END AS is_invalid_trip_sequence,

    CASE
        WHEN request_datetime > on_scene_datetime
          OR on_scene_datetime > pickup_datetime
          OR pickup_datetime > dropoff_datetime
        THEN TRUE
        ELSE FALSE
    END AS has_invalid_timestamp_sequence,

    CASE
        WHEN base_passenger_fare < 0
        THEN TRUE
        ELSE FALSE
    END AS is_negative_base_passenger_fare,

    CASE
        WHEN driver_pay < 0
        THEN TRUE
        ELSE FALSE
    END AS is_negative_driver_pay

FROM staging.fhvhv_trips;