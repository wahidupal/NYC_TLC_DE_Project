import duckdb

con = duckdb.connect()

query = """
SELECT
    column_name,
    null_count,
    ROUND(100.0 * null_count / total_rows, 2) AS null_percentage
FROM (
    SELECT
        COUNT(*) AS total_rows,
        COUNT(*) - COUNT(VendorID) AS VendorID,
        COUNT(*) - COUNT(tpep_pickup_datetime) AS pickup_datetime,
        COUNT(*) - COUNT(tpep_dropoff_datetime) AS dropoff_datetime,
        COUNT(*) - COUNT(passenger_count) AS passenger_count,
        COUNT(*) - COUNT(trip_distance) AS trip_distance,
        COUNT(*) - COUNT(RatecodeID) AS RatecodeID,
        COUNT(*) - COUNT(store_and_fwd_flag) AS store_and_fwd_flag,
        COUNT(*) - COUNT(PULocationID) AS PULocationID,
        COUNT(*) - COUNT(DOLocationID) AS DOLocationID,
        COUNT(*) - COUNT(payment_type) AS payment_type,
        COUNT(*) - COUNT(fare_amount) AS fare_amount,
        COUNT(*) - COUNT(extra) AS extra,
        COUNT(*) - COUNT(mta_tax) AS mta_tax,
        COUNT(*) - COUNT(tip_amount) AS tip_amount,
        COUNT(*) - COUNT(tolls_amount) AS tolls_amount,
        COUNT(*) - COUNT(improvement_surcharge) AS improvement_surcharge,
        COUNT(*) - COUNT(total_amount) AS total_amount,
        COUNT(*) - COUNT(congestion_surcharge) AS congestion_surcharge,
        COUNT(*) - COUNT(Airport_fee) AS Airport_fee,
        COUNT(*) - COUNT(cbd_congestion_fee) AS cbd_congestion_fee
    FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
)
UNPIVOT (
    null_count FOR column_name IN (
        VendorID,
        pickup_datetime,
        dropoff_datetime,
        passenger_count,
        trip_distance,
        RatecodeID,
        store_and_fwd_flag,
        PULocationID,
        DOLocationID,
        payment_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        congestion_surcharge,
        Airport_fee,
        cbd_congestion_fee
    )
)
ORDER BY null_count DESC;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()