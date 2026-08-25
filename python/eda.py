import duckdb

con = duckdb.connect()
query = """
SELECT *
FROM read_parquet('../data/raw/fhv_tripdata_2026-01.parquet')
WHERE dropOff_datetime < pickup_datetime;
"""

result = con.execute(query).fetchdf()

print(result.to_string(index=False))

con.close()

# con = duckdb.connect()
# query = """
# SUMMARIZE
# SELECT *
# FROM read_parquet('../data/raw/fhvhv_tripdata_2026-01.parquet');
# """

# result = con.execute(query).fetchdf()

# print(result.to_string(index=False))

# con.close()

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


