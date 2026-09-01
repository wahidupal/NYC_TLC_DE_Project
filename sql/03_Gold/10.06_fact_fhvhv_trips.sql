-- ============================================================
-- 10.06 FHVHV Trip Fact
-- ============================================================
-- Purpose:
-- Create the Gold fact table for High Volume For-Hire Vehicle
-- (FHVHV) trips.
--
-- Grain:
-- One row represents one FHVHV trip.
--
-- Source:
-- cleaned.fhvhv_trips_clean
--
-- Location descriptions remain in gold.dim_location.
-- Location IDs are retained as foreign-key-style references.
--
-- Timestamp and financial anomalies are preserved through
-- dedicated data-quality flags.
-- ============================================================


DROP TABLE IF EXISTS gold.fact_fhvhv_trips;


CREATE TABLE gold.fact_fhvhv_trips AS

SELECT

    -- --------------------------------------------------------
    -- Identifiers
    -- --------------------------------------------------------

    hvfhv_license_number AS hvfhs_license_number,

    dispatching_base_number,

    originating_base_number,

    -- --------------------------------------------------------
    -- Trip timestamps
    -- --------------------------------------------------------

    request_datetime,

    on_scene_datetime,

    pickup_datetime,

    dropoff_datetime,

    -- --------------------------------------------------------
    -- Operational timing metrics
    -- --------------------------------------------------------

    request_to_on_scene_seconds,

    on_scene_to_pickup_seconds,

    trip_duration_seconds,

    -- --------------------------------------------------------
    -- Location keys
    -- --------------------------------------------------------

    pickup_location_id,

    dropoff_location_id,

    -- --------------------------------------------------------
    -- Trip characteristics
    -- --------------------------------------------------------

    trip_miles AS trip_distance_miles,

    trip_time AS trip_time_seconds,

    -- --------------------------------------------------------
    -- Financial measures
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
    -- Timestamp-quality flags
    -- --------------------------------------------------------

    is_invalid_request_sequence,

    is_invalid_on_scene_sequence,

    is_invalid_trip_sequence,

    has_invalid_timestamp_sequence,

    -- --------------------------------------------------------
    -- Financial-quality flags
    -- --------------------------------------------------------

    is_negative_base_passenger_fare,

    is_negative_driver_pay

FROM cleaned.fhvhv_trips_clean;