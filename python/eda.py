import duckdb

con = duckdb.connect()
query = """
SELECT
    PUlocationID,
    COUNT(*) AS trip_count
FROM read_parquet('../data/raw/fhv_tripdata_2026-01.parquet')
GROUP BY PUlocationID
ORDER BY trip_count DESC
LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

con = duckdb.connect()
query = """
SELECT
    DOlocationID,
    COUNT(*) AS trip_count
FROM read_parquet('../data/raw/fhv_tripdata_2026-01.parquet')
GROUP BY DOlocationID
ORDER BY trip_count DESC
LIMIT 20;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# con = duckdb.connect()
# query = """
# SELECT COUNT(*) AS trips_fhv_tripdata
# FROM read_parquet('../data/raw/fhv_tripdata_2026-01.parquet');
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()

# con = duckdb.connect()
# query = """
# SELECT COUNT(*) AS trips_fhvhv_tripdata
# FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()


