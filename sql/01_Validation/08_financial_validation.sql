-- ============================================================
-- 08. Financial / Reconciliation Validation
-- ============================================================
-- Purpose:
-- Validate financial relationships in the staging datasets
-- after ingestion.
--
-- This validation distinguishes between:
--
--   1. Financial reconciliation discrepancies
--      -> REVIEW rather than automatic failure.
--
--      The individual financial components do not always
--      reconcile exactly to total_amount using a simple
--      arithmetic sum. During EDA, systematic differences
--      were observed in the source data (e.g. +2.50, -3.25,
--      -2.50). Therefore, reconciliation discrepancies are
--      flagged for investigation rather than treated as
--      ingestion errors.
--
--   2. Negative financial values
--      -> REVIEW rather than automatic failure, because
--         refunds, reversals and adjustments may legitimately
--         produce negative amounts.
--
-- The purpose is therefore to identify records requiring
-- investigation without incorrectly modifying or removing
-- legitimate source transactions.
-- ============================================================


WITH financial_checks AS (

    -- --------------------------------------------------------
    -- Yellow Taxi
    -- --------------------------------------------------------
    --
    -- Reconciliation check:
    --
    -- Compare total_amount against the sum of the available
    -- financial components.
    --
    -- This is an investigative check rather than a strict
    -- business-rule validation because the source data contains
    -- systematic reconciliation differences.
    --
    -- A small tolerance is used because the source contains
    -- floating-point values.
    -- --------------------------------------------------------

    SELECT
        'yellow_trips' AS dataset,
        'total_amount_reconciliation' AS check_name,
        COUNT(*) FILTER (
            WHERE ABS(
                total_amount
                - (
                    COALESCE(fare_amount, 0)
                    + COALESCE(extra, 0)
                    + COALESCE(mta_tax, 0)
                    + COALESCE(tip_amount, 0)
                    + COALESCE(tolls_amount, 0)
                    + COALESCE(improvement_surcharge, 0)
                    + COALESCE(congestion_surcharge, 0)
                    + COALESCE(airport_fee, 0)
                    + COALESCE(cbd_congestion_fee, 0)
                )
            ) > 0.02
        ) AS violation_count
    FROM staging.yellow_trips


    UNION ALL


    -- --------------------------------------------------------
    -- Green Taxi
    -- --------------------------------------------------------

    SELECT
        'green_trips',
        'total_amount_reconciliation',
        COUNT(*) FILTER (
            WHERE ABS(
                total_amount
                - (
                    COALESCE(fare_amount, 0)
                    + COALESCE(extra, 0)
                    + COALESCE(mta_tax, 0)
                    + COALESCE(tip_amount, 0)
                    + COALESCE(tolls_amount, 0)
                    + COALESCE(improvement_surcharge, 0)
                    + COALESCE(congestion_surcharge, 0)
                    + COALESCE(cbd_congestion_fee, 0)
                )
            ) > 0.02
        )
    FROM staging.green_trips


    UNION ALL


    -- --------------------------------------------------------
    -- Yellow negative financial records
    -- --------------------------------------------------------

    SELECT
        'yellow_trips',
        'negative_total_amount',
        COUNT(*) FILTER (
            WHERE total_amount < 0
        )
    FROM staging.yellow_trips


    UNION ALL


    -- --------------------------------------------------------
    -- Green negative financial records
    -- --------------------------------------------------------

    SELECT
        'green_trips',
        'negative_total_amount',
        COUNT(*) FILTER (
            WHERE total_amount < 0
        )
    FROM staging.green_trips


    UNION ALL


    -- --------------------------------------------------------
    -- FHVHV negative base passenger fare
    -- --------------------------------------------------------

    SELECT
        'fhvhv_trips',
        'negative_base_passenger_fare',
        COUNT(*) FILTER (
            WHERE base_passenger_fare < 0
        )
    FROM staging.fhvhv_trips


    UNION ALL


    -- --------------------------------------------------------
    -- FHVHV negative driver pay
    -- --------------------------------------------------------

    SELECT
        'fhvhv_trips',
        'negative_driver_pay',
        COUNT(*) FILTER (
            WHERE driver_pay < 0
        )
    FROM staging.fhvhv_trips

)


-- ============================================================
-- Final Validation Result
-- ============================================================

SELECT
    dataset,
    check_name,
    violation_count,

    CASE
        -- Financial anomalies are investigative findings,
        -- not automatic ingestion failures.
        WHEN check_name IN (
            'total_amount_reconciliation',
            'negative_total_amount',
            'negative_base_passenger_fare',
            'negative_driver_pay'
        )
        THEN 'REVIEW'

        WHEN violation_count = 0
        THEN 'PASS'

        ELSE 'FAIL'
    END AS validation_status

FROM financial_checks

ORDER BY
    dataset,
    check_name;