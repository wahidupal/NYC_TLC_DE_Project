SELECT
    COUNT(*) AS rows_with_missing_location
FROM analytics.zone_performance
WHERE pickup_location_id IS NULL
   OR borough IS NULL
   OR zone IS NULL
   OR service_zone IS NULL;