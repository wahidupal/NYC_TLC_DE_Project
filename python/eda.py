import duckdb

con = duckdb.connect()

query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) - COUNT(VendorID) AS VendorID_nulls,
    COUNT(*) - COUNT(tpep_pickup_datetime) AS pickup_datetime_nulls,
    COUNT(*) - COUNT(tpep_dropoff_datetime) AS dropoff_datetime_nulls,
    COUNT(*) - COUNT(passenger_count) AS passenger_count_nulls,
    COUNT(*) - COUNT(trip_distance) AS trip_distance_nulls,
    COUNT(*) - COUNT(RatecodeID) AS RatecodeID_nulls,
    COUNT(*) - COUNT(store_and_fwd_flag) AS store_and_fwd_flag_nulls,
    COUNT(*) - COUNT(PULocationID) AS PULocationID_nulls,
    COUNT(*) - COUNT(DOLocationID) AS DOLocationID_nulls,
    COUNT(*) - COUNT(payment_type) AS payment_type_nulls,
    COUNT(*) - COUNT(fare_amount) AS fare_amount_nulls,
    COUNT(*) - COUNT(extra) AS extra_nulls,
    COUNT(*) - COUNT(mta_tax) AS mta_tax_nulls,
    COUNT(*) - COUNT(tip_amount) AS tip_amount_nulls,
    COUNT(*) - COUNT(tolls_amount) AS tolls_amount_nulls,
    COUNT(*) - COUNT(improvement_surcharge) AS improvement_surcharge_nulls,
    COUNT(*) - COUNT(total_amount) AS total_amount_nulls,
    COUNT(*) - COUNT(congestion_surcharge) AS congestion_surcharge_nulls,
    COUNT(*) - COUNT(Airport_fee) AS Airport_fee_nulls,
    COUNT(*) - COUNT(cbd_congestion_fee) AS cbd_congestion_fee_nulls
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()