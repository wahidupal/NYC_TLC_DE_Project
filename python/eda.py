import duckdb

con = duckdb.connect()
query = """
DESCRIBE SELECT *

FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet')
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# con = duckdb.connect()
# query = """
# SELECT
#     dispatching_base_num,
#     COUNT(*) AS trip_count
# FROM read_parquet('../data/raw/fhv_tripdata_2026-01.parquet')
# GROUP BY dispatching_base_num
# ORDER BY trip_count DESC
# LIMIT 20;
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()

# con = duckdb.connect()
# query = """
# SELECT
#     Affiliated_base_number,
#     COUNT(*) AS trip_count
# FROM read_parquet('../data/raw/fhv_tripdata_2026-01.parquet')
# GROUP BY Affiliated_base_number
# ORDER BY trip_count DESC
# LIMIT 20;
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()

# con = duckdb.connect()
# query = """
# SELECT
#     COUNT(*) AS total_trips,
#     COUNT(*) FILTER (
#         WHERE dispatching_base_num <> Affiliated_base_number
#     ) AS different_base_trips
# FROM read_parquet('../data/raw/fhv_tripdata_2026-01.parquet')
# WHERE Affiliated_base_number IS NOT NULL;
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()


