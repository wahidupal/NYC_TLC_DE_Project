## Analytics Layer

The Analytics layer provides business-facing datasets built from the validated Gold layer. While the Gold layer is designed around reusable facts and dimensions, the Analytics layer applies aggregation and business-oriented transformations to support reporting, operational analysis, and ad-hoc SQL analysis.

The analytical models are intentionally kept focused rather than creating a large number of overlapping summary tables.

### 11.01 Daily Trip Performance

**Model:** `analytics.daily_trip_performance`

**Grain:** One row per date and service type.

This model provides a daily view of trip activity across Yellow Taxi, Green Taxi, FHV, and FHVHV services.

Key metrics include:

* Trip count
* Total distance
* Average distance
* Total duration
* Average duration
* Day of week
* Weekend indicator

The model applies the January 2026 reporting boundary at the Analytics layer. This allows the Gold layer to preserve valid source records that fall outside the reporting period while ensuring analytical outputs represent the intended reporting month.

### 11.02 Zone Performance

**Model:** `analytics.zone_performance`

**Grain:** One row per date, service type, and pickup location.

This model provides a geographic view of service activity using the NYC TLC Taxi Zone Lookup data.

Key metrics include:

* Trip count
* Total distance
* Average distance
* Total duration
* Average duration
* Borough
* Zone
* Service zone

Pickup location is used as the primary geographic dimension. Dropoff-based analysis can be derived separately when destination-focused questions are required.

The model also preserves differences between source datasets. For example, FHV does not provide trip distance, so its distance metrics remain `NULL` rather than being calculated or imputed.

FHV also contains a substantial number of trips with missing pickup locations in the source data. These records are not assigned to an artificial `Unknown` location. Consequently, the FHV zone model represents only trips for which a usable pickup location is available.

### 11.03 Hourly Trip Performance

**Model:** `analytics.hourly_trip_performance`

**Grain:** One row per date, hour, and service type.

This model supports time-of-day analysis and allows trip activity to be compared across the four service types.

Key metrics include:

* Trip count
* Total distance
* Average distance
* Total duration
* Average duration
* Hour of day
* Day of week
* Weekend indicator

The model covers the 24-hour day using hours `0` through `23`. Some date-hour combinations may be absent when no trips occurred during that period rather than being artificially populated with zero-volume records.

The model was validated against `analytics.daily_trip_performance`, with trip totals reconciling exactly for all four services. Small differences in aggregated distance and duration are attributable to rounding at different aggregation levels.

### 11.04 Route Performance

**Model:** `analytics.route_performance`

**Grain:** One row per service type, pickup location, and dropoff location.

This model provides route-level analysis by combining pickup and dropoff locations with the Taxi Zone Lookup dimension.

Key metrics include:

* Trip count
* Total distance
* Average distance
* Total duration
* Average duration
* Pickup borough and zone
* Dropoff borough and zone

The same physical `gold.dim_location` table is joined twice, once in the role of pickup location and once in the role of dropoff location. This is a role-playing dimension pattern and avoids maintaining separate physical location dimensions for the same underlying reference data.

For FHV, route-level analysis is limited to trips with both pickup and dropoff locations available. Since FHV does not provide trip distance, its route distance metrics remain `NULL`.

### Analytical Design Principles

The Analytics layer follows several principles:

1. **Business-facing grain**
   Each model has an explicitly defined grain so that users can understand what one row represents before querying the data.

2. **Reuse Gold rather than duplicate source logic**
   Analytical models are built from validated Gold facts and dimensions rather than directly from raw source tables.

3. **Preserve source limitations**
   Missing or unavailable source attributes are preserved rather than artificially generated or imputed without justification.

4. **Separate reporting filters from data preservation**
   The January 2026 reporting boundary is applied in the Analytics layer, while valid source records outside the reporting period remain available in Gold for traceability and investigation.

5. **Cross-model reconciliation**
   Analytical aggregations are validated against lower-level models to ensure that transformations do not introduce unexplained differences.

Together, the four models provide complementary analytical perspectives:

**Time → Location → Hour → Route**

This gives the warehouse a compact set of reusable analytical outputs without creating redundant summary models.
