import duckdb

con = duckdb.connect()

result = con.execute("""
    DESCRIBE
    SELECT *
    FROM read_parquet('../data/raw/yellow_tripdata_2026-01.parquet');
""").fetchdf()

print(result.to_string(index=False))

con.close()