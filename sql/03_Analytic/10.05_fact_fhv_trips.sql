-- ============================================================
-- 10.05 FHV Trip Fact
-- ============================================================
-- Purpose:
-- Create the Gold fact table for For-Hire Vehicle (FHV) trips.
--
-- Grain:
-- One row represents one FHV trip.
--
-- Source:
-- cleaned.fhv_trips_clean
--
-- Location descriptions remain in gold.dim_location.
-- Location IDs are retained as foreign-key-style references.
-- ============================================================


DROP TABLE IF EXISTS gold.fact_fhv_trips;


CREATE TABLE gold.fact_fhv_trips AS

SELECT

    -- --------------------------------------------------------
    -- Identifiers
    -- --------------------------------------------------------

    dispatching_base_number,

    affiliated_base_number,

    sr_flag,

    -- --------------------------------------------------------
    -- Trip timestamps
    -- --------------------------------------------------------

    pickup_datetime,

    dropoff_datetime,

    -- --------------------------------------------------------
    -- Derived trip metrics
    -- --------------------------------------------------------

    trip_duration_seconds,

    -- --------------------------------------------------------
    -- Location keys
    -- --------------------------------------------------------

    pickup_location_id,

    dropoff_location_id,

    -- --------------------------------------------------------
    -- Data-quality flags
    -- --------------------------------------------------------

    is_invalid_timestamp

FROM cleaned.fhv_trips_clean;