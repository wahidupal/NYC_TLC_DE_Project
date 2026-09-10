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
