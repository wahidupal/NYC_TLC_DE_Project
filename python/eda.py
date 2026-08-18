import duckdb

con = duckdb.connect()

query = """
SELECT
    payment_type,
    COUNT(*) AS trip_count
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY payment_type
ORDER BY payment_type;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()

query = """
SELECT
    payment_type,
    COUNT(*) AS trips,

    SUM(total_amount) AS total_revenue,

    SUM(congestion_surcharge) AS congestion_revenue,

    SUM(Airport_fee) AS airport_fee_revenue

FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet')
GROUP BY payment_type
ORDER BY payment_type;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()