DROP TABLE IF EXISTS analytics.zone_performance;

CREATE TABLE analytics.zone_performance AS

WITH yellow AS (

    SELECT
        d.date,
        d.year,
        d.month,
        d.month_name,
        d.day_name,
        d.is_weekend,
        'Yellow' AS service_type,
        y.pickup_location_id,
        l.borough,
        l.zone,
        l.service_zone,
        COUNT(*) AS trip_count,
        ROUND(SUM(y.trip_distance_miles)::numeric, 2)
            AS total_distance_miles,
        ROUND(AVG(y.trip_distance_miles)::numeric, 2)
            AS avg_distance_miles,
        ROUND((SUM(y.trip_duration_seconds) / 60.0)::numeric, 2)
            AS total_duration_minutes,
        ROUND((AVG(y.trip_duration_seconds) / 60.0)::numeric, 2)
            AS avg_duration_minutes
    FROM gold.fact_yellow_trips y

    JOIN gold.dim_date d
        ON DATE(y.pickup_datetime) = d.date

    LEFT JOIN gold.dim_location l
        ON y.pickup_location_id = l.location_id

    WHERE d.date >= '2026-01-01'
      AND d.date < '2026-02-01'

    GROUP BY
        d.date,
        d.year,
        d.month,
        d.month_name,
        d.day_name,
        d.is_weekend,
        y.pickup_location_id,
        l.borough,
        l.zone,
        l.service_zone
),

green AS (

    SELECT
        d.date,
        d.year,
        d.month,
        d.month_name,
        d.day_name,
        d.is_weekend,
        'Green' AS service_type,
        g.pickup_location_id,
        l.borough,
        l.zone,
        l.service_zone,
        COUNT(*) AS trip_count,
        ROUND(SUM(g.trip_distance_miles)::numeric, 2)
            AS total_distance_miles,
        ROUND(AVG(g.trip_distance_miles)::numeric, 2)
            AS avg_distance_miles,
        ROUND((SUM(g.trip_duration_seconds) / 60.0)::numeric, 2)
            AS total_duration_minutes,
        ROUND((AVG(g.trip_duration_seconds) / 60.0)::numeric, 2)
            AS avg_duration_minutes
    FROM gold.fact_green_trips g

    JOIN gold.dim_date d
        ON DATE(g.pickup_datetime) = d.date

    LEFT JOIN gold.dim_location l
        ON g.pickup_location_id = l.location_id

    WHERE d.date >= '2026-01-01'
      AND d.date < '2026-02-01'

    GROUP BY
        d.date,
        d.year,
        d.month,
        d.month_name,
        d.day_name,
        d.is_weekend,
        g.pickup_location_id,
        l.borough,
        l.zone,
        l.service_zone
),

fhv AS (

    SELECT
        d.date,
        d.year,
        d.month,
        d.month_name,
        d.day_name,
        d.is_weekend,
        'FHV' AS service_type,
        f.pickup_location_id,
        l.borough,
        l.zone,
        l.service_zone,
        COUNT(*) AS trip_count,

        NULL::numeric AS total_distance_miles,
        NULL::numeric AS avg_distance_miles,

        ROUND((SUM(f.trip_duration_seconds) / 60.0)::numeric, 2)
            AS total_duration_minutes,
        ROUND((AVG(f.trip_duration_seconds) / 60.0)::numeric, 2)
            AS avg_duration_minutes

    FROM gold.fact_fhv_trips f

    JOIN gold.dim_date d
        ON DATE(f.pickup_datetime) = d.date

    LEFT JOIN gold.dim_location l
        ON f.pickup_location_id = l.location_id

    WHERE d.date >= '2026-01-01'
      AND d.date < '2026-02-01'
      AND f.pickup_location_id IS NOT NULL

    GROUP BY
        d.date,
        d.year,
        d.month,
        d.month_name,
        d.day_name,
        d.is_weekend,
        f.pickup_location_id,
        l.borough,
        l.zone,
        l.service_zone
),

fhvhv AS (

    SELECT
        d.date,
        d.year,
        d.month,
        d.month_name,
        d.day_name,
        d.is_weekend,
        'FHVHV' AS service_type,
        h.pickup_location_id,
        l.borough,
        l.zone,
        l.service_zone,
        COUNT(*) AS trip_count,
        ROUND(SUM(h.trip_distance_miles)::numeric, 2)
            AS total_distance_miles,
        ROUND(AVG(h.trip_distance_miles)::numeric, 2)
            AS avg_distance_miles,
        ROUND((SUM(h.trip_duration_seconds) / 60.0)::numeric, 2)
            AS total_duration_minutes,
        ROUND((AVG(h.trip_duration_seconds) / 60.0)::numeric, 2)
            AS avg_duration_minutes

    FROM gold.fact_fhvhv_trips h

    JOIN gold.dim_date d
        ON DATE(h.pickup_datetime) = d.date

    LEFT JOIN gold.dim_location l
        ON h.pickup_location_id = l.location_id

    WHERE d.date >= '2026-01-01'
      AND d.date < '2026-02-01'

    GROUP BY
        d.date,
        d.year,
        d.month,
        d.month_name,
        d.day_name,
        d.is_weekend,
        h.pickup_location_id,
        l.borough,
        l.zone,
        l.service_zone
)

SELECT * FROM yellow

UNION ALL

SELECT * FROM green

UNION ALL

SELECT * FROM fhv

UNION ALL

SELECT * FROM fhvhv

ORDER BY
    date,
    service_type,
    pickup_location_id;