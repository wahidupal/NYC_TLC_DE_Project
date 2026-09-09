## 🔍 Data Quality & Validation

Data quality was treated as a core part of the pipeline rather than a final cleanup step. The validation process was designed to identify structural problems, source-data anomalies, and inconsistencies introduced during transformation.

A key principle throughout the project was:

> **Invalid ≠ unusual.**

Records with clear integrity violations were removed during the cleaning process. However, unusual observations were not automatically deleted using arbitrary thresholds. When a record could not be proven invalid, it was retained and the limitation was documented.

### Validation Approach

The pipeline applies validation checks across several dimensions:

* Row-count reconciliation between pipeline layers
* Date and timestamp validation
* Null and completeness checks
* Location-ID validation and enrichment
* Trip-duration validation
* Distance-distribution analysis
* Financial reconciliation
* Cross-layer aggregation reconciliation
* Source-specific business-rule checks

The objective was not simply to make every validation query return zero anomalies. Instead, validation was used to understand **what the data contains, whether an observation is actually invalid, and how the issue should be handled downstream**.

---

### Row-Count & Transformation Reconciliation

Row counts were compared across staging, cleaned, Gold, and Analytics layers to ensure that transformations behaved as intended.

For example, the Yellow Taxi dataset contained **3,724,889** staging records. Only one record was removed during cleaning because its pickup timestamp occurred after its drop-off timestamp.

Similarly, the Analytics layer applies an explicit **January 2026 reporting boundary**. This is important because the TLC source files can contain records outside the nominal monthly reporting period.

The Gold layer therefore preserves source records, while analytical models explicitly define their reporting period.

---

### Timestamp & Duration Validation

Trip timestamps were examined for:

* Missing pickup or drop-off timestamps
* Pickup occurring after drop-off
* Zero-duration trips
* Extremely long durations

The distinction between invalid and unusual observations was particularly important here.

For Yellow Taxi, **45,070 records** had pickup timestamps greater than or equal to drop-off timestamps. Investigation showed that only **one record had pickup after drop-off**. The remaining **45,069 records had exactly zero duration** and were therefore retained rather than incorrectly classified as invalid.

For FHV, the data contained highly unusual durations. The maximum observed duration was approximately **1,096 days**, including records with pickup and drop-off timestamps separated by multiple years.

These observations are clearly implausible as normal trips, but the timestamps still satisfy the basic ordering rule of pickup occurring before drop-off. They were therefore retained and documented as source-data anomalies rather than removed through an arbitrary duration threshold.

FHVHV contained one zero-duration trip. Since its pickup and drop-off timestamps were identical and there was no negative duration, the record was retained.

---

### Location Validation

Location IDs were validated against the Taxi Zone Lookup table to distinguish between missing source data and failed dimensional mapping.

For Yellow, Green, and FHVHV, the available pickup location IDs could be mapped successfully to the location dimension.

FHV required special treatment. Approximately **1.65 million FHV records have NULL pickup locations**. Investigation showed that these were source-level NULLs rather than unmapped TLC location IDs.

Consequently, the pipeline does not invent an `Unknown` location to make those records appear geographically complete.

The FHV zone and route analytics therefore represent only the subset of records for which the required location information exists, while the overall FHV trip population remains available in the underlying fact data.

---

### Distance Validation

Distance distributions were analyzed for the datasets where trip distance is available.

The investigation revealed extreme values in both Yellow and Green Taxi data. For example, the maximum Yellow Taxi distance was approximately **269,097 miles**.

Rather than applying an arbitrary rule such as:

`distance > 50 miles → remove`

the pipeline retains these observations.

This decision was deliberate. Some genuinely long NYC taxi trips exist, particularly trips involving airports and locations outside the normal Manhattan travel pattern. A simple distance threshold could therefore remove legitimate observations together with erroneous source records.

The extreme values are documented as source-data anomalies and should be considered when interpreting distance-based averages and other sensitive metrics.

For FHV, trip distance is not available in the source data used by this project. Distance metrics therefore remain NULL rather than being estimated or fabricated.

---

### Financial Reconciliation

Financial fields were also checked for internal consistency.

Several source-specific issues were identified, including negative amounts and recurring differences between component fare fields and reported total amounts.

For Yellow Taxi, the reconciliation difference was not uniformly zero. The investigation found recurring differences such as **+$2.50** and **-$3.25**, alongside other smaller differences.

These patterns indicated that the discrepancy could not safely be treated as simple data corruption. Instead of loosening the reconciliation tolerance until the validation passed, the issue was retained as a documented source-specific accounting limitation.

This prevents the pipeline from hiding potentially meaningful differences simply to achieve a zero-error validation result.

---

### Validation of Analytical Models

The Analytics layer was independently reconciled against the underlying Gold data.

For example:

* Daily trip totals were reconciled against hourly trip totals.
* January trip populations were reconciled between Daily, Zone, Hourly, and Route models.
* Pickup and drop-off locations were checked against `dim_location`.
* Aggregated distance and duration values were compared across analytical grains.

The trip-count reconciliations between the Daily and Hourly models returned **no discrepancies**.

Small differences observed when reconciling rounded distance and duration aggregates were attributable to rounding at different aggregation levels rather than missing or duplicated records.

---

### Handling Strategy

The resulting handling strategy can be summarized as follows:

| Data condition                               | Treatment                                  |
| -------------------------------------------- | ------------------------------------------ |
| Pickup timestamp after drop-off              | Remove                                     |
| Zero-duration trip                           | Retain and flag/investigate                |
| Missing source location                      | Preserve NULL and document                 |
| Unmapped location ID                         | Investigate as dimensional integrity issue |
| Extreme distance                             | Retain and document                        |
| Extreme duration                             | Retain and document                        |
| Unavailable source attribute                 | Preserve as NULL                           |
| Financial reconciliation anomaly             | Investigate and document                   |
| Valid source records outside reporting month | Preserve in Gold; filter in Analytics      |

This approach preserves the distinction between **data correction**, **data validation**, and **analytical filtering**.

Rather than attempting to make the source data look artificially clean, the pipeline preserves traceability to the original data while applying stricter rules where there is clear evidence of invalidity.
