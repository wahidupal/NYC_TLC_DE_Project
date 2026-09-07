DROP TABLE IF EXISTS analytics.route_performance;

CREATE TABLE analytics.route_performance AS

WITH yellow AS (

    SELECT
        'Yellow' AS service_type,

        y.pickup_location_id,
        pl.borough AS pickup_borough,
        pl.zone AS pickup_zone,

        y.dropoff_location_id,
        dl.borough AS dropoff_borough,
        dl.zone AS dropoff_zone,

        COUNT(*) AS trip_count,

        ROUND(
            SUM(y.trip_distance_miles)::numeric,
            2
        ) AS total_distance_miles,

        ROUND(
            AVG(y.trip_distance_miles)::numeric,
            2
        ) AS avg_distance_miles,

        ROUND(
            (SUM(y.trip_duration_seconds) / 60.0)::numeric,
            2
        ) AS total_duration_minutes,

        ROUND(
            (AVG(y.trip_duration_seconds) / 60.0)::numeric,
            2
        ) AS avg_duration_minutes

    FROM gold.fact_yellow_trips y

    JOIN gold.dim_location pl
        ON y.pickup_location_id = pl.location_id

    JOIN gold.dim_location dl
        ON y.dropoff_location_id = dl.location_id

    WHERE y.pickup_datetime >= '2026-01-01'
      AND y.pickup_datetime < '2026-02-01'

    GROUP BY
        y.pickup_location_id,
        pl.borough,
        pl.zone,
        y.dropoff_location_id,
        dl.borough,
        dl.zone
),


green AS (

    SELECT
        'Green' AS service_type,

        g.pickup_location_id,
        pl.borough AS pickup_borough,
        pl.zone AS pickup_zone,

        g.dropoff_location_id,
        dl.borough AS dropoff_borough,
        dl.zone AS dropoff_zone,

        COUNT(*) AS trip_count,

        ROUND(
            SUM(g.trip_distance_miles)::numeric,
            2
        ) AS total_distance_miles,

        ROUND(
            AVG(g.trip_distance_miles)::numeric,
            2
        ) AS avg_distance_miles,

        ROUND(
            (SUM(g.trip_duration_seconds) / 60.0)::numeric,
            2
        ) AS total_duration_minutes,

        ROUND(
            (AVG(g.trip_duration_seconds) / 60.0)::numeric,
            2
        ) AS avg_duration_minutes

    FROM gold.fact_green_trips g

    JOIN gold.dim_location pl
        ON g.pickup_location_id = pl.location_id

    JOIN gold.dim_location dl
        ON g.dropoff_location_id = dl.location_id

    WHERE g.pickup_datetime >= '2026-01-01'
      AND g.pickup_datetime < '2026-02-01'

    GROUP BY
        g.pickup_location_id,
        pl.borough,
        pl.zone,
        g.dropoff_location_id,
        dl.borough,
        dl.zone
),


fhv AS (

    SELECT
        'FHV' AS service_type,

        f.pickup_location_id,
        pl.borough AS pickup_borough,
        pl.zone AS pickup_zone,

        f.dropoff_location_id,
        dl.borough AS dropoff_borough,
        dl.zone AS dropoff_zone,

        COUNT(*) AS trip_count,

        NULL::numeric AS total_distance_miles,
        NULL::numeric AS avg_distance_miles,

        ROUND(
            (SUM(f.trip_duration_seconds) / 60.0)::numeric,
            2
        ) AS total_duration_minutes,

        ROUND(
            (AVG(f.trip_duration_seconds) / 60.0)::numeric,
            2
        ) AS avg_duration_minutes

    FROM gold.fact_fhv_trips f

    JOIN gold.dim_location pl
        ON f.pickup_location_id = pl.location_id

    JOIN gold.dim_location dl
        ON f.dropoff_location_id = dl.location_id

    WHERE f.pickup_datetime >= '2026-01-01'
      AND f.pickup_datetime < '2026-02-01'

    GROUP BY
        f.pickup_location_id,
        pl.borough,
        pl.zone,
        f.dropoff_location_id,
        dl.borough,
        dl.zone
),


fhvhv AS (

    SELECT
        'FHVHV' AS service_type,

        h.pickup_location_id,
        pl.borough AS pickup_borough,
        pl.zone AS pickup_zone,

        h.dropoff_location_id,
        dl.borough AS dropoff_borough,
        dl.zone AS dropoff_zone,

        COUNT(*) AS trip_count,

        ROUND(
            SUM(h.trip_distance_miles)::numeric,
            2
        ) AS total_distance_miles,

        ROUND(
            AVG(h.trip_distance_miles)::numeric,
            2
        ) AS avg_distance_miles,

        ROUND(
            (SUM(h.trip_duration_seconds) / 60.0)::numeric,
            2
        ) AS total_duration_minutes,

        ROUND(
            (AVG(h.trip_duration_seconds) / 60.0)::numeric,
            2
        ) AS avg_duration_minutes

    FROM gold.fact_fhvhv_trips h

    JOIN gold.dim_location pl
        ON h.pickup_location_id = pl.location_id

    JOIN gold.dim_location dl
        ON h.dropoff_location_id = dl.location_id

    WHERE h.pickup_datetime >= '2026-01-01'
      AND h.pickup_datetime < '2026-02-01'

    GROUP BY
        h.pickup_location_id,
        pl.borough,
        pl.zone,
        h.dropoff_location_id,
        dl.borough,
        dl.zone
)

SELECT * FROM yellow

UNION ALL

SELECT * FROM green

UNION ALL

SELECT * FROM fhv

UNION ALL

SELECT * FROM fhvhv;