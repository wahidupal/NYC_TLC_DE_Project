## Repository Structure

The repository separates ingestion code, exploratory analysis, SQL transformations, source data, and project documentation.

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
└── Technical Decisions.md
```

### Directory Overview

| Directory / File          | Purpose                                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `data/raw/`               | Source reference data used by the pipeline. Large TLC trip Parquet files are not committed because of their size.                      |
| `docs/`                   | Architecture and data-model diagrams, including editable draw.io source files and rendered images.                                     |
| `python/`                 | Exploratory data analysis scripts and supporting EDA work performed during source investigation.                                       |
| `src/ingestion/`          | Python ingestion code used to read source files with DuckDB and load them into PostgreSQL.                                             |
| `sql/01_Validation/`      | Data-quality checks, reconciliation queries, anomaly investigation, and domain validation.                                             |
| `sql/02_Cleaned_layer/`   | Source-specific cleaning, standardization, derived fields, and preparation for dimensional modelling.                                  |
| `sql/03_Gold/`            | Gold-layer dimensional models, including reusable fact and dimension tables.                                                           |
| `sql/04_Analytic/`        | Business-facing analytical models for daily, hourly, zone, and route analysis.                                                         |
| `README.md`               | Main project documentation and entry point for the repository.                                                                         |
| Documentation `.md` files | Detailed documentation covering architecture, integration, data modelling, data quality, technical decisions, and the Analytics layer. |

### SQL Transformation Structure

The SQL directories mirror the major transformation stages of the warehouse:

**Validation → Cleaned → Gold → Analytics**

The validation layer is intentionally kept as a separate stage because data-quality investigation is treated as part of the engineering workflow rather than as an implicit step inside transformation queries.
