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

con = duckdb.connect()
query = """
SELECT
    COUNT(*) FILTER (WHERE passenger_count IS NULL) AS passenger_nulls,
    COUNT(*) FILTER (WHERE RatecodeID IS NULL) AS ratecode_nulls,
    COUNT(*) FILTER (WHERE store_and_fwd_flag IS NULL) AS flag_nulls,
    COUNT(*) FILTER (WHERE congestion_surcharge IS NULL) AS congestion_nulls,
    COUNT(*) FILTER (WHERE Airport_fee IS NULL) AS airport_nulls,

    COUNT(*) FILTER (
        WHERE passenger_count IS NULL
          AND RatecodeID IS NULL
          AND store_and_fwd_flag IS NULL
          AND congestion_surcharge IS NULL
          AND Airport_fee IS NULL
    ) AS all_five_null
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    COUNT(*) FILTER (
        WHERE passenger_count IS NULL
          AND (
                RatecodeID IS NOT NULL
             OR store_and_fwd_flag IS NOT NULL
             OR congestion_surcharge IS NOT NULL
             OR Airport_fee IS NOT NULL
          )
    ) AS passenger_null_but_others_not_null
FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# So all for all five columns here in the dataset has the exact same number of NULL values, 1.088M. All of these NULLs happens in the same rows in these columns
