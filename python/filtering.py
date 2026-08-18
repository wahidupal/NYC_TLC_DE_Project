import duckdb

con = duckdb.connect()

query = """
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (
        WHERE passenger_count IS NULL
          AND RatecodeID IS NULL
          AND store_and_fwd_flag IS NULL
          AND congestion_surcharge IS NULL
          AND Airport_fee IS NULL
    ) AS all_five_null,
    COUNT(*) FILTER (
        WHERE passenger_count IS NULL
           OR RatecodeID IS NULL
           OR store_and_fwd_flag IS NULL
           OR congestion_surcharge IS NULL
           OR Airport_fee IS NULL
    ) AS at_least_one_null
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()