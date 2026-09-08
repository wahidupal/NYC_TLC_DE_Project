# Project Overview and Dataset Overview


# 🚕 NYC TLC Data Pipeline

## Overview

This project builds an end-to-end data pipeline for integrating multiple NYC Taxi & Limousine Commission (TLC) trip datasets into a unified, analytics-ready data warehouse.

The NYC TLC publishes trip data for multiple transportation services, including **Yellow Taxi, Green Taxi, For-Hire Vehicles (FHV), and High-Volume For-Hire Vehicles (FHVHV)**. While these datasets describe similar transportation activity, they differ in structure, available fields, and data quality characteristics.

The goal of this project was to design a pipeline capable of handling these differences and transforming the source datasets into a common analytical model.

The pipeline covers the full journey from raw source files to analytical reporting:

**Raw Parquet Files → Ingestion → Validation → Standardization → Data Warehouse → Dimensional Modeling → Analytics**

The final warehouse follows a layered architecture and provides a unified trip model that supports analysis across all available transportation services.

---

## 🎯 Project Objectives

The main objectives of this project were to:

* Integrate multiple heterogeneous NYC TLC transportation datasets into a unified data model.
* Handle differences in source schemas and data availability across services.
* Validate data quality throughout the pipeline rather than assuming source data is clean.
* Standardize the datasets into a common trip structure.
* Build a dimensional model optimized for analytical queries.
* Create reusable analytical datasets for daily, hourly, zone, and route-level analysis.
* Practice real-world SQL, data modeling, data validation, and data engineering concepts using a large public dataset.

---

# 📊 Dataset Overview

The project integrates five NYC TLC datasets:

| Dataset             | Description                                                         |
| ------------------- | ------------------------------------------------------------------- |
| 🚕 Yellow Taxi      | Traditional NYC yellow taxi trip records                            |
| 🟢 Green Taxi       | NYC green taxi trip records                                         |
| 🚐 FHV              | Traditional For-Hire Vehicle trip records                           |
| 🚗 FHVHV            | High-Volume For-Hire Vehicle trip records                           |
| 📍 Taxi Zone Lookup | Geographic lookup table used to enrich pickup and dropoff locations |

The four trip datasets represent different transportation services and do not share identical schemas.

For example, some services provide trip distance information while others do not. Location information is also not equally complete across all datasets.

These differences make direct integration impossible without schema standardization and service-specific transformation logic.

### Key Dataset Differences

| Service Type | Trip Distance | Pickup Location Coverage | Dropoff Location Coverage |
| ------------ | ------------: | -----------------------: | ------------------------: |
| Yellow       |     Available |                Available |                 Available |
| Green        |     Available |                Available |                 Available |
| FHV          | Not available |      Partially available |       Partially available |
| FHVHV        |     Available |                Available |                 Available |

Rather than forcing all services into identical source-level structures, the pipeline preserves these differences where necessary while standardizing the fields required for unified analysis.

The resulting model allows all services to be analyzed together while correctly representing missing or unavailable information.

---

## 🔄 Pipeline Overview

The pipeline transforms the raw NYC TLC datasets through multiple layers:

```text
NYC TLC Source Data
        │
        ▼
Python + DuckDB Ingestion
        │
        ▼
Data Validation & Quality Checks
        │
        ▼
Schema Standardization
        │
        ▼
Common Trip Structure
        │
        ▼
PostgreSQL Data Warehouse
        │
        ▼
Gold Dimensional Model
        │
        ▼
Analytics Layer
        │
        ├── Daily Performance
        ├── Hourly Performance
        ├── Zone Performance
        └── Route Performance
```
