-- ============================================================
-- 10.02 Location Dimension
-- ============================================================
-- Purpose:
-- Create the Gold location dimension from the validated
-- staging taxi zone lookup.
--
-- This dimension provides descriptive information for the
-- LocationID values used by the TLC trip datasets.
--
-- The staging table remains unchanged.
-- ============================================================


DROP TABLE IF EXISTS gold.dim_location;


CREATE TABLE gold.dim_location AS

SELECT
    location_id,
    borough,
    zone,
    service_zone

FROM staging.taxi_zone_lookup;