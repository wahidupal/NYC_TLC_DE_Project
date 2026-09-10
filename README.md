# 🚕 NYC TLC Data Engineering Pipeline

An end-to-end data engineering project that ingests, validates, transforms, and models **26.6M+ NYC transportation trip records** from four heterogeneous TLC datasets into a PostgreSQL data warehouse.

## Project Overview

The NYC Taxi & Limousine Commission (TLC) publishes trip records for several transportation services, including Yellow Taxi, Green Taxi, For-Hire Vehicles (FHV), and High-Volume For-Hire Vehicles (FHVHV).

Although these datasets describe similar transportation activity, they differ significantly in schema, available attributes, location coverage, timestamp structure, and data quality characteristics.

This project builds a complete data pipeline to handle those differences while preserving important source-level information.

The pipeline takes the datasets from raw Parquet and CSV files through:

**Source Data → Ingestion → Validation → Cleaning → Dimensional Modeling → Analytics**

The warehouse is implemented in **PostgreSQL**, with **Python and DuckDB** used for source-file ingestion and exploration. The final Gold layer uses a dimensional model with separate fact tables for each transportation service and shared date and location dimensions. An Analytics layer then provides reusable datasets for daily, hourly, zone-level, and route-level analysis.

A major focus of the project is **data quality**. Instead of assuming that unusual records are automatically errors, the pipeline distinguishes between objectively invalid records and suspicious but potentially meaningful source observations. Invalid records are removed where the business or data constraints make their invalidity clear, while unusual source behaviour is retained, investigated, and documented.

## Key Engineering Highlights

* **26.6M+ trip records** processed across Yellow Taxi, Green Taxi, FHV, and FHVHV datasets.
* **Heterogeneous source integration** with service-specific schemas, fields, and data availability.
* **Python + DuckDB ingestion** for efficient reading and processing of large Parquet and CSV source files.
* **PostgreSQL data warehouse** with separate Staging, Cleaned, Gold, and Analytics layers.
* **Dimensional modelling** using service-specific fact tables and shared `dim_date` and `dim_location` dimensions.
* **Extensive data-quality validation**, including timestamp consistency, duration checks, financial reconciliation, location coverage, null analysis, and sequence validation.
* **Source anomaly investigation** rather than blindly applying arbitrary cleaning thresholds.
* **Reusable Analytics models** for daily, hourly, zone, and route-level performance analysis.
* **Reproducible ingestion and transformation workflow** using version-controlled Python and SQL scripts.
* **Documented technical decisions** explaining why records were removed, retained, transformed, or flagged.

## 🏗️ Architecture

The pipeline follows a layered data warehouse architecture designed to separate source ingestion, data quality processing, analytical modelling, and business-facing datasets.

```text
NYC TLC Source Data
        │
        ▼
┌───────────────────────┐
│ Python + DuckDB       │
│ Source Ingestion      │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ PostgreSQL            │
│ Staging Layer         │
│ Source-level data     │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Cleaned Layer         │
│ Standardization       │
│ Derived fields        │
│ Data-quality handling │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Gold Layer            │
│ Dimensional Model     │
│                       │
│ 4 Service Facts       │
│ + Shared Dimensions   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Analytics Layer       │
│                       │
│ Daily                 │
│ Hourly                │
│ Zone                  │
│ Route                 │
└───────────────────────┘
```

The architecture follows a **Medallion-style data lifecycle**, while the Gold layer uses **dimensional modelling** for analytical workloads.

These are complementary concepts rather than competing architectures:

* **Staging** preserves the source data after ingestion.
* **Cleaned** standardizes fields, derives reusable attributes, and handles objective data-quality issues.
* **Gold** organizes the data into service-specific fact tables and shared dimensions.
* **Analytics** provides business-oriented datasets built from the Gold layer.

Detailed architecture and data-flow documentation is available in the project documentation.

---

## 📊 Dataset Overview

The project uses four NYC TLC trip-record datasets covering **January 2026**, together with the TLC Taxi Zone Lookup table.

| Dataset          | Service            | Trip Distance | Location Coverage | Key Characteristics                                                     |
| ---------------- | ------------------ | ------------: | ----------------- | ----------------------------------------------------------------------- |
| Yellow Taxi      | Yellow taxi        |     Available | High              | Detailed trip, fare, payment, and location information                  |
| Green Taxi       | Green taxi         |     Available | High              | Similar trip structure to Yellow Taxi with service-specific differences |
| FHV              | For-Hire Vehicle   | Not available | Partial           | Large number of missing locations and source-provided timestamps        |
| FHVHV            | High-Volume FHV    |     Available | High              | Detailed request, on-scene, pickup, and dropoff lifecycle               |
| Taxi Zone Lookup | Location reference |           N/A | N/A               | Maps TLC location IDs to boroughs and zone names                        |

The datasets are similar enough to support cross-service analysis, but they are **not interchangeable**.

For example:

* FHV does not provide trip distance.
* FHV contains substantial missing pickup and dropoff information.
* FHVHV contains additional lifecycle timestamps that allow request, on-scene, pickup, and dropoff sequences to be validated.
* Yellow and Green Taxi contain fare and payment information that is not available in the same form across all services.
* Different datasets contain different types of source anomalies and quality limitations.

The pipeline therefore does **not** force every source into an identical structure simply for the sake of consistency. Instead, common analytical concepts are standardized while service-specific information and limitations are preserved.

### Why this matters

A data warehouse should not hide important characteristics of its source data.

For example, replacing missing FHV distance values with zero would make the dataset appear complete while introducing false information. The Gold model instead preserves the limitation and allows downstream analytical models to handle it explicitly.

This principle is used throughout the project:

> **Preserve what the source tells us, remove what is objectively invalid, document what is suspicious, and apply business-specific filtering at the analytical layer.**

---

## 🔍 Data Quality and Validation

Data quality was treated as a core engineering component rather than a final cleanup step.

Validation checks were performed at multiple stages of the pipeline, including:

* Row-count reconciliation between layers
* Null and missing-value analysis
* Timestamp validity and chronological ordering
* Trip duration validation
* Negative duration detection
* Negative financial values
* Financial reconciliation
* Pickup and dropoff location coverage
* Taxi-zone mapping validation
* Distance distribution analysis
* Outlier and anomaly investigation
* FHVHV lifecycle sequence validation
* Source-date boundary checks

### Invalid vs. unusual data

One of the main design decisions in this project was to distinguish between **invalid** and **unusual** records.

A record that violates an objective integrity rule can be removed. For example, a trip where the pickup timestamp occurs after the dropoff timestamp is objectively invalid.

An unusually large distance or duration, however, is not automatically invalid. Removing every statistical outlier would risk deleting genuine source observations and hiding data-quality problems.

Therefore:

* **Objectively invalid records** are removed where the rule is unambiguous.
* **Suspicious records** are retained when their validity cannot be conclusively disproved.
* **Anomalies are investigated and documented** rather than silently discarded.
* **Analytical models apply business-specific filtering** when a particular use case requires a representative subset.

This approach allows the warehouse to remain faithful to the source while making its limitations visible to downstream users.

## 📈 Analytics Layer

The Analytics layer transforms the reusable Gold models into datasets designed for common operational and analytical questions.

The models are intentionally kept at different grains rather than forcing all analysis into one wide table.

| Model                     | Grain                                | Purpose                                                    |
| ------------------------- | ------------------------------------ | ---------------------------------------------------------- |
| `daily_trip_performance`  | Date × Service                       | Daily trip volume, distance, and duration performance      |
| `hourly_trip_performance` | Date × Hour × Service                | Identify hourly demand patterns and peak periods           |
| `zone_performance`        | Date × Service × Pickup Zone         | Compare activity and trip characteristics across locations |
| `route_performance`       | Service × Pickup Zone × Dropoff Zone | Analyze movement between origin and destination zones      |

The Analytics layer also applies **business-specific reporting boundaries**. For example, the source files are preserved as received, while analytical models can restrict the reporting period to January 2026.

This separation prevents reporting requirements from contaminating the underlying warehouse and keeps the Gold layer reusable for future analysis.

Detailed definitions, grain decisions, reconciliation checks, and model outputs are documented in the Analytics Layer documentation.

---

## 🛠️ Technology Stack

### Data Processing

* **Python** for ingestion utilities, exploratory data analysis, and data-processing logic
* **DuckDB** for efficient querying and inspection of Parquet and CSV source files
* **Pandas** for exploratory analysis and data investigation

### Data Warehouse

* **PostgreSQL** as the central relational data warehouse
* SQL for validation, transformation, dimensional modelling, and analytical models

### Data Modelling

* Medallion-style layered architecture
* Dimensional modelling
* Star-schema design
* Service-specific fact tables
* Shared date and location dimensions

### Development & Documentation

* Git and GitHub for version control
* Draw.io for architecture and data-model diagrams
* Markdown for technical documentation

---

## 📁 Repository Structure

```text
NYC_TLC_DE_Project/
│
├── data/
│   └── raw/
│       └── taxi_zone_lookup.csv
│
├── docs/
│   ├── images/
│   ├── Data Integration.drawio
│   ├── Data model diagram.drawio
│   ├── Gold Data Model.drawio
│   └── Medalion Architecture.drawio
│
├── python/
│   ├── EDA check list.txt
│   ├── eda.py
│   ├── fhv_eda.py
│   ├── fhvhv_eda.py
│   ├── filtering.py
│   ├── yellow_eda.py
│   └── yellow_taxi_eda.py
│
├── src/
│   └── ingestion/
│       ├── config.py
│       └── load_source_file.py
│
├── sql/
│   ├── 01_Validation/
│   ├── 02_Cleaned_layer/
│   ├── 03_Gold/
│   └── 04_Analytic/
│
├── .gitignore
├── README.md
├── Analytics Layer.md
├── Architecture & Data Flow.md
├── Data Integration.md
├── Data Model.md
├── Data Quality & Validation.md
├── Repository Structure.md
├── Setup & Reproducibility.md
└── Technical Decisions.md
```

### Directory Responsibilities

**`data/raw/`**
Contains source files required by the pipeline. Large TLC Parquet files are intentionally excluded from Git.

**`python/`**
Contains exploratory analysis and data-investigation scripts developed during the project.

**`src/ingestion/`**
Contains the reusable source-ingestion code used to load files into PostgreSQL staging tables.

**`sql/01_Validation/`**
Contains data-quality and source-validation checks.

**`sql/02_Cleaned_layer/`**
Contains cleaning, standardization, derived fields, and source-specific transformation logic.

**`sql/03_Gold/`**
Contains dimensional warehouse models, including the service-specific fact tables and shared dimensions.

**`sql/04_Analytic/`**
Contains business-facing analytical models built from the Gold layer.

**`docs/`**
Contains architecture and data-model diagrams and supporting project documentation.

---

## 📚 Detailed Documentation

The README provides the high-level view of the project. Detailed technical decisions, validation findings, modelling choices, and reproducibility instructions are documented separately.

* **Architecture & Data Flow**
  Pipeline architecture, layer responsibilities, and data movement.

* **Data Integration**
  How the four heterogeneous transportation datasets are integrated while preserving service-specific characteristics.

* **Data Model**
  Gold-layer dimensional model, fact tables, dimensions, grain, and relationships.

* **Data Quality & Validation**
  Validation framework, anomalies, reconciliation findings, and decisions about invalid versus unusual records.

* **Analytics Layer**
  Analytical model definitions, grain, reconciliation, and business use cases.

* **Technical Decisions**
  Major architecture, modelling, ingestion, and data-quality decisions and their rationale.

* **Setup & Reproducibility**
  Environment setup, source-data requirements, database creation, ingestion commands, and pipeline execution.

* **Repository Structure**
  Explanation of the project directory and file organization.
