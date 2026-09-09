## Technical Decisions

The project was designed around the characteristics and limitations of the source data rather than forcing the datasets into a uniform structure. The following decisions were made to keep the pipeline reproducible, analytically useful, and defensible.

### PostgreSQL as the Data Warehouse

PostgreSQL was selected as the central analytical warehouse because the project focuses heavily on relational data modelling, SQL transformations, data validation, and analytical querying.

It provides a suitable environment for implementing the staging, cleaned, Gold, and Analytics layers while also serving as the SQL environment for downstream analysis and interview practice.

### DuckDB for File-Based Data Processing

DuckDB is used alongside Python during ingestion to efficiently inspect and process the TLC Parquet files before loading the data into PostgreSQL.

This is particularly useful for the TLC datasets because the source files are distributed as Parquet and can be large. DuckDB provides SQL-based access to these files without requiring the complete datasets to be loaded into memory through pandas.

Python is used to orchestrate the ingestion process and load the resulting data into PostgreSQL.

### Medallion-Style Layered Architecture

The pipeline uses a layered architecture consisting of:

**Staging → Cleaned → Gold → Analytics**

The layers separate different responsibilities:

* **Staging:** Preserve the source data in a queryable form.
* **Cleaned:** Standardize fields, derive reusable attributes, and handle objectively invalid records.
* **Gold:** Provide validated dimensional and fact models for analytical reuse.
* **Analytics:** Provide business-facing aggregations for common analytical questions.

This separation makes it easier to trace transformations and distinguish source preservation from analytical modelling.

### Separate Fact Tables for Each Service

The four trip datasets are not forced into a single physical `fact_trips` table.

Instead, the Gold layer contains separate service-specific facts:

* `gold.fact_yellow_trips`
* `gold.fact_green_trips`
* `gold.fact_fhv_trips`
* `gold.fact_fhvhv_trips`

Although the datasets share common analytical concepts, their source schemas and available attributes differ significantly.

For example, FHV does not provide trip distance, while Yellow, Green, and FHVHV do. FHV also contains substantially more missing location information.

Keeping the facts separate preserves these source-specific characteristics while allowing the Analytics layer to standardize the concepts required for cross-service comparisons.

### Shared Date and Location Dimensions

Common reference data is modelled through reusable dimensions:

* `gold.dim_date`
* `gold.dim_location`

The location dimension is based on the NYC TLC Taxi Zone Lookup dataset and is used for both pickup and dropoff locations.

Rather than creating separate physical pickup and dropoff dimensions, the same dimension is used in different roles. This is a **role-playing dimension** pattern and avoids duplicating the same reference data.

### Preserve Source Limitations Instead of Inventing Data

The pipeline does not attempt to manufacture values that are unavailable in the source datasets.

For example, FHV does not contain trip-distance information. Its distance-related analytical fields therefore remain `NULL`.

Similarly, a large number of FHV records have missing pickup locations. These records are not assigned to an artificial `Unknown` zone merely to make the dataset appear complete.

This preserves the distinction between:

* a value that genuinely does not exist in the source,
* a value that is missing in the source,
* and a value that failed dimensional mapping.

### Invalid Records vs. Unusual Records

The project deliberately distinguishes objectively invalid records from unusual observations.

Records with clear integrity violations, such as a pickup timestamp occurring after the dropoff timestamp, are removed during cleaning.

Unusual observations are generally retained when they are technically valid but suspicious.

Examples include:

* Extremely large trip distances in Yellow and Green Taxi data.
* FHV records with implausibly long durations spanning months or years.
* Zero-duration trips.
* Financial component totals that do not always reconcile exactly with the reported total.

These observations are documented and investigated rather than removed using arbitrary thresholds.

This approach avoids introducing analyst-defined assumptions into the source data simply to produce cleaner-looking distributions.

### No Arbitrary Distance Threshold

Extreme trip distances were investigated separately rather than applying a rule such as:

`distance > 50 miles → invalid`

Such a rule would be difficult to justify because legitimate long-distance trips exist, particularly trips involving airports and locations outside the city.

The pipeline therefore retains extreme distance observations in the Gold layer and documents their effect on aggregate metrics such as average distance.

Analytical models that require representative distance statistics can apply an explicit quality rule appropriate to that particular use case rather than silently deleting source records during the core transformation process.

### Reporting Period vs. Source Data Preservation

The source files are treated as the source of truth for the records they contain, rather than assuming that every row in a monthly file must fall strictly within the calendar month implied by the filename.

Some Yellow and Green Taxi records were found outside the January 2026 reporting period.

These records are preserved in the lower and Gold layers where appropriate, while the Analytics layer explicitly applies the January 2026 reporting boundary.

This separates **data preservation** from **reporting requirements**.

### Financial Reconciliation Is Investigated, Not Forced

Financial validation identified recurring differences between component-level amounts and reported total amounts in Yellow and Green Taxi data, as well as negative financial values in some datasets.

The pipeline does not simply loosen reconciliation tolerances until the checks pass.

Instead, recurring patterns were investigated and documented as source-data accounting behaviour or anomalies requiring further interpretation.

This prevents a validation rule from being weakened merely to achieve a green validation result.

### Validation Before Analytical Consumption

Analytical models are built from validated Gold data rather than directly from the source tables.

Validation includes:

* Row-count reconciliation
* Timestamp integrity
* Duration checks
* Location mapping
* Source completeness
* Distance anomaly analysis
* Financial reconciliation
* Cross-layer aggregation checks

For example, daily and hourly trip totals were reconciled to verify that the aggregation logic did not introduce unexplained changes in trip volume.

### Avoiding Redundant Analytical Models

The Analytics layer intentionally contains four focused models:

* `daily_trip_performance`
* `zone_performance`
* `hourly_trip_performance`
* `route_performance`

A separate overall service-performance summary was considered but not implemented because it would largely duplicate information already available in the daily performance model.

The goal is to provide reusable analytical datasets without creating a large collection of overlapping summary tables.

### Design Philosophy

The overall design principle is:

> **Preserve what the source tells us, remove what is objectively invalid, document what is suspicious, and apply business-specific filtering at the analytical layer.**

This keeps the pipeline transparent and makes analytical assumptions explicit rather than hiding them inside transformation logic.
