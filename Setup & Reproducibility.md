# Setup & Reproducibility

This guide explains how to reproduce the NYC TLC Data Engineering pipeline using the original public datasets.

The project integrates five source datasets:

* Yellow Taxi trip records
* Green Taxi trip records
* For-Hire Vehicle (FHV) trip records
* High-Volume For-Hire Vehicle (FHVHV) trip records
* NYC Taxi Zone Lookup

The project was developed using **January 2026 trip data**.

---

## 1. Prerequisites

To reproduce the project, you will need:

* Python 3
* PostgreSQL
* DuckDB
* Access to the NYC TLC public datasets

The project uses:

| Component                    | Technology     |
| ---------------------------- | -------------- |
| Source files                 | Parquet / CSV  |
| Exploratory analysis         | Python         |
| Source file processing       | DuckDB         |
| Data warehouse               | PostgreSQL     |
| Database connection          | psycopg2       |
| Configuration                | python-dotenv  |
| Transformation and modelling | SQL            |
| Analytics                    | PostgreSQL SQL |

---

## 2. Download the Source Data

The raw datasets are intentionally **not included in this GitHub repository** because of their large file sizes.

The data is publicly available from the official NYC Taxi & Limousine Commission:

[NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page?utm_source=chatgpt.com)

Download the following January 2026 datasets:

* `yellow_tripdata_2026-01.parquet`
* `green_tripdata_2026-01.parquet`
* `fhv_tripdata_2026-01.parquet`
* `fhvhv_tripdata_2026-01.parquet`

Also download:

* `taxi_zone_lookup.csv`

Place the files in:

```text
data/raw/
```

The expected structure is:

```text
data/
└── raw/
    ├── yellow_tripdata_2026-01.parquet
    ├── green_tripdata_2026-01.parquet
    ├── fhv_tripdata_2026-01.parquet
    ├── fhvhv_tripdata_2026-01.parquet
    └── taxi_zone_lookup.csv
```

> **Note:** The raw files are excluded from the repository to keep the project lightweight. The original NYC TLC website remains the authoritative source for downloading the data.

---

## 3. Exploratory Data Analysis

Before building the database pipeline, exploratory data analysis was performed on the source datasets.

The four NYC TLC trip datasets do not share an identical structure. The exploratory analysis was therefore used to understand:

* Source schemas
* Column differences between services
* Null patterns
* Date coverage
* Trip-distance distributions
* Trip-duration distributions
* Location availability
* Extreme observations
* Source-specific limitations

This analysis informed the later validation and modelling decisions.

For example:

* FHV does not provide trip-distance data.
* FHV contains a large number of missing pickup location values.
* The four services have different source schemas and available attributes.
* Extreme distance and duration values exist in the source data.

EDA was an important part of the initial development process. It helped determine how the heterogeneous source datasets could be integrated without artificially treating them as identical.

---

# 4. Create the PostgreSQL Database

Create the PostgreSQL database:

```sql
CREATE DATABASE NYC_TLC;
```

Connect to the database before creating the warehouse schemas and tables.

The pipeline uses PostgreSQL as the central analytical data warehouse.

---

# 5. Configure Database Credentials

Database credentials are loaded using environment variables rather than being stored directly in the Python source code.

The ingestion configuration uses:

```python
load_dotenv()
```

Create a `.env` file containing your PostgreSQL connection details:

```text
PG_HOST=localhost
PG_PORT=5432
PG_DATABASE=NYC_TLC
PG_USER=your_username
PG_PASSWORD=your_password
```

The `config.py` file loads these values into the PostgreSQL connection configuration.

```text
src/
└── ingestion/
    ├── config.py
    └── load_source_file.py
```

> **Important:** **Do not commit** your `.env` file or database credentials to GitHub.

The `.env` file should be included in `.gitignore`.

---

# 6. Create the Database Structure

Before loading the source data, create the required PostgreSQL schemas and staging tables.

The ingestion script inserts the datasets into the following tables:

| Dataset          | Target Table               |
| ---------------- | -------------------------- |
| Yellow Taxi      | `staging.yellow_trips`     |
| Green Taxi       | `staging.green_trips`      |
| FHV              | `staging.fhv_trips`        |
| FHVHV            | `staging.fhvhv_trips`      |
| Taxi Zone Lookup | `staging.taxi_zone_lookup` |

Run the staging-layer SQL scripts before starting ingestion.

The source-specific staging tables preserve the original structure of each dataset.

---

# 7. Install Python Dependencies

The ingestion process requires the following Python packages:

```bash
pip install duckdb psycopg2-binary python-dotenv
```

These libraries are used for:

* `duckdb` — reading Parquet and CSV source files
* `psycopg2` — connecting Python to PostgreSQL
* `python-dotenv` — loading database credentials from environment variables

---

# 8. Run Data Ingestion

The ingestion script loads **one dataset at a time**.

The script:

1. Reads the source file using DuckDB.
2. Retrieves the source columns dynamically.
3. Connects to PostgreSQL.
4. Inserts records into the corresponding staging table.
5. Loads records in batches of 10,000 rows.
6. Commits the transaction after ingestion is complete.

From the ingestion directory, run:

### Yellow Taxi

```bash
python load_source_file.py yellow
```

### Green Taxi

```bash
python load_source_file.py green
```

### FHV

```bash
python load_source_file.py fhv
```

### FHVHV

```bash
python load_source_file.py fhvhv
```

### Taxi Zone Lookup

```bash
python load_source_file.py taxi_zone_lookup
```

The script will display ingestion progress:

```text
Dataset: yellow
Columns: ...

Inserted: 10,000 rows
Inserted: 20,000 rows
...

Total rows inserted: ...
Ingestion complete.
```

---

# 9. Run Data Quality Validation

After ingestion, run the validation queries against the staging data.

Validation was performed before building the downstream data models.

The validation process includes checks for:

* Row counts
* Date coverage
* Null values
* Location mapping
* Trip duration
* Trip distance
* Extreme observations
* Source-specific data characteristics

The validation approach does not assume that every unusual value should automatically be deleted.

The project distinguishes between:

* Invalid records
* Extreme but source-preserved observations
* Expected source limitations
* Missing values that are characteristic of a particular service

For example:

* FHV does not contain trip-distance information.
* Many FHV records have missing pickup locations.
* Extreme Yellow Taxi distance observations remain documented rather than being deleted using arbitrary thresholds.
* Extreme FHV trip durations were investigated and documented.

The validation process supports the principle of preserving source data while identifying and documenting important quality issues.

---

# 10. Build the Cleaned Layer

After validation, run the Cleaned layer transformations.

The Cleaned layer prepares the source-specific datasets for integration and dimensional modelling.

Typical transformations include:

* Column standardization
* Source normalization
* Derived attributes
* Trip-duration calculations
* Timestamp preparation
* Preparation for integration

The four services are not forced into an artificially identical structure.

Instead, the transformations preserve meaningful differences between the sources.

---

# 11. Build the Gold Layer

After the Cleaned layer is complete, build the Gold layer.

The Gold layer contains the reusable facts and dimensions used for analysis.

The dimensional model includes:

* `dim_date`
* `dim_location`
* Unified trip fact data

The location dimension supports both pickup and dropoff analysis through role-playing relationships.

The Gold layer provides a consistent analytical structure while preserving important source characteristics.

For example, FHV records do not receive artificially generated distance values simply because the other services provide trip-distance information.

---

# 12. Build the Analytics Layer

The Analytics layer contains aggregated datasets designed for analytical queries and reporting.

The project currently includes:

### Daily Trip Performance

Analysis by:

* Date
* Service type

### Zone Performance

Analysis by:

* Date
* Service type
* Pickup location

### Hourly Trip Performance

Analysis by:

* Date
* Hour
* Service type

### Route Performance

Analysis by:

* Service type
* Pickup location
* Dropoff location

Each analytical model is validated using reconciliation checks against the underlying Gold-layer data.

---

# Recommended Execution Order

The complete workflow is:

```text
1. Download NYC TLC source data
            ↓
2. Perform proper exploratory data analysis
            ↓
3. Create PostgreSQL database
            ↓
4. Configure .env credentials
            ↓
5. Create staging schemas and tables
            ↓
6. Run Python + DuckDB ingestion
            ↓
7. Validate staging data
            ↓
8. Build the Cleaned layer
            ↓
9. Build the Gold layer
            ↓
10. Build the Analytics layer
```

---

# Reproducibility Notes

The project is reproducible using the original public NYC TLC datasets and the repository's Python and SQL code.

The raw datasets are intentionally excluded from GitHub because of their size.

Depending on your environment, you may need to adjust:

* PostgreSQL credentials
* Python environment
* Local file paths
* PostgreSQL version
* Package installation

The ingestion script currently expects the January 2026 source files to be available in:

```text
data/raw/
```

The NYC TLC website remains the authoritative source for obtaining the original trip record data.
