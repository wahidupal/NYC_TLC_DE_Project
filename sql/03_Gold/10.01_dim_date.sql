-- ============================================================
-- 10.01 Gold - Date Dimension
-- ============================================================
-- Purpose:
-- Create a reusable calendar dimension for the Gold layer.
--
-- The date dimension supports time-based analysis across all
-- TLC datasets without repeatedly deriving calendar attributes
-- from individual trip tables.
-- ============================================================


DROP TABLE IF EXISTS gold.dim_date;


CREATE TABLE gold.dim_date AS

SELECT
    TO_CHAR(date_value, 'YYYYMMDD')::INTEGER AS date_key,

    date_value AS date,

    EXTRACT(YEAR FROM date_value)::INTEGER AS year,

    EXTRACT(MONTH FROM date_value)::INTEGER AS month,

    TO_CHAR(date_value, 'Month') AS month_name,

    EXTRACT(DAY FROM date_value)::INTEGER AS day,

    TO_CHAR(date_value, 'Day') AS day_name,

    EXTRACT(ISODOW FROM date_value)::INTEGER AS day_of_week,

    EXTRACT(WEEK FROM date_value)::INTEGER AS week_of_year,

    EXTRACT(QUARTER FROM date_value)::INTEGER AS quarter,

    CASE
        WHEN EXTRACT(ISODOW FROM date_value) IN (6, 7)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend

FROM GENERATE_SERIES(
    '2025-12-01'::DATE,
    '2026-02-28'::DATE,
    INTERVAL '1 day'
) AS date_series(date_value);