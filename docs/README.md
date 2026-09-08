# NYC TLC Data Pipeline

An end-to-end data pipeline that integrates four disparate NYC Taxi & Limousine Commission (TLC) trip datasets — Yellow Taxi, Green Taxi, FHV, and FHVHV — plus the Taxi Zone Lookup table, into a unified analytics-ready warehouse.

Raw Parquet files are ingested with Python and DuckDB, validated, staged, cleaned, and modeled into a dimensional (star schema) gold layer, which powers a set of independent performance reports consumed via SQL/BI.

> **Note:** All diagrams below are written in [Mermaid](https://mermaid.js.org/), which GitHub renders natively — no external image files needed. If a diagram doesn't render, view this file directly on GitHub rather than in a plain text editor.

---

## 1. Architecture at a Glance

The pipeline follows a **medallion architecture**: raw source data moves through progressively refined layers until it's ready for consumption.

```mermaid
flowchart TD
    SRC[Data Source<br/>Yellow / Green / FHV / FHVHV / Zone Lookup] --> BRONZE[Bronze Layer<br/>Raw Data]
    BRONZE --> SILVER[Silver Layer<br/>Clean & Standardize]
    SILVER --> GOLD[Gold Layer<br/>Facts & Dimensions]
    GOLD --> ANALYTICS[Analytics Layer<br/>Aggregated Metrics]
    ANALYTICS --> CONSUME[Consumption<br/>SQL / BI / Insights]
```

---

## 2. Detailed Data Flow

Zooming into the bronze → silver transition: ingested data passes through a dedicated **data quality & validation** step before it's accepted into staging.

```mermaid
flowchart TD
    SRC["NYC TLC Source Data<br/>Yellow Taxi Trips, Green Taxi Trips,<br/>FHV Trips, FHVHV Trips, Taxi Zone Lookup"] -->|Download / load| ING[Python + DuckDB<br/>Read, inspect, handle schema, load]
    ING -->|Ingest| STAGE[Staging Schema<br/>Raw source table, source-specific structure]
    ING --> DQ["Data Quality & Validation<br/>Row reconciliation, null checks,<br/>location / duration / distance checks"]
    DQ --> STAGE
    STAGE -->|Clean & transform| CLEAN[Cleaned Schema<br/>Standardized columns, derived durations,<br/>data prep, source normalization]
    CLEAN -->|Model| GOLD[Gold Schema<br/>Facts & Dimensions]
    GOLD -->|Aggregate / analyze| ANALYTICS[Analytics Schema]
    ANALYTICS --> SQL[SQL Consumption<br/>Business analysis, ad-hoc queries, BI / reporting]
```

---

## 3. Gold Layer: Dimensional Data Model

The gold layer is a star schema. `dim_location` is a **role-playing dimension** — the same physical table is joined twice into the fact table, once for the pickup location and once for the dropoff location.

```mermaid
erDiagram
    DIM_DATE ||--o{ FACT_TRIPS : "date_key"
    DIM_LOCATION_PICKUP ||--o{ FACT_TRIPS : "pickup_location_id"
    DIM_LOCATION_DROPOFF ||--o{ FACT_TRIPS : "dropoff_location_id"

    DIM_DATE {
        int date_key PK
        date date
        int year
        int month
        string month_name
        string day_name
        boolean is_weekend
    }

    DIM_LOCATION_PICKUP {
        int location_id PK
        string borough
        string zone
        string service_zone
    }

    DIM_LOCATION_DROPOFF {
        int location_id PK
        string borough
        string zone
        string service_zone
    }

    FACT_TRIPS {
        datetime pickup_datetime
        datetime dropoff_datetime
        float trip_distance_miles
        int trip_duration_seconds
        int pickup_location_id FK
        int dropoff_location_id FK
        string service_type
    }
```

---

## 4. Gold-to-Analytics Lineage

This is the full lineage from raw dimensions through to reporting. The four performance reports are **independent of one another** — each is derived directly from the analytics layer, not from combining the others.

```mermaid
flowchart TD
    subgraph GOLD["Gold Layer — Star Schema"]
        direction LR
        DD[dim_date] --> FT[Unified Trip Facts / fact_trips]
        DLP[dim_location - Pickup] --> FT
        DLD[dim_location - Dropoff] --> FT
    end

    FT --> AL[Analytics Layer]
    AL --> DP[Daily Performance]
    AL --> HP[Hourly Performance]
    AL --> ZP[Zone Performance]
    AL --> RP[Route Performance]
```

---

## 5. Tech Stack

| Layer | Tooling |
|---|---|
| Ingestion | Python, DuckDB |
| Validation | Python (row reconciliation, null / location / duration / distance checks) |
| Warehouse | PostgreSQL |
| Modeling | Dimensional (star schema) — facts & dimensions |
| Consumption | SQL, BI tooling |

---

## 6. Repository Structure

```
.
├── ingestion/          # Python + DuckDB source-reading and loading scripts
├── validation/         # Data quality checks
├── sql/
│   ├── staging/        # Staging schema DDL
│   ├── cleaned/        # Cleaned schema transformations
│   ├── gold/           # Fact and dimension table DDL + models
│   └── analytics/      # Aggregated reporting views
└── README.md
```

---

## About This Project

This project was built to practice integrating multiple heterogeneous NYC TLC trip datasets into a single coherent warehouse, following medallion architecture and dimensional modeling best practices — from raw Parquet ingestion through to a query-ready analytics layer.
