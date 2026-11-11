# Rolling Monitoring IoT Data

Continuous Intelligence | Project 04 | Customized Report

## Overview

This project builds an automated data pipeline using Polars to process 15-minute IoT sensor logs. It handles two primary tasks:
Time-Series Resampling to roll up high-frequency data into hourly or daily averages to surface long-term trends, and Device Profiling
to group records by unique sensor IDs and compute target performance metrics like average temperature, maximum humidity, and total active
operational runtime.

## Data

The example dataset contains 600 time-ordered observations
collected at fifteen-minute intervals.

Each observation includes:

- `timestamp` -     timestamp 15 minute cadence
- `sensor_id` -     SENS-01...SENS12
- `temperature_c` - temp reading in °C
- `humidity` -      total response time in milliseconds.
- `battery_pct` -   Battery level, trends downward over the file
- `status` -        ok, low_battery (below 15%) or error (rare)
- Source: [sample sensor](https://howtocsv.com/sample-sensors-csv/)

[View Example Dataset](https://github.com/itsanibose/cintel-04-sensor-monitoring/blob/main/data/sample-sensors.csv)

## Methods

The pipeline groups records by unique sensor profiles, truncates timestamps into explicit historical steps,
and applies multi-level window calculations across the fleet timeline.

Rolling averages are calculated using a configurable window size for:

- Ambient temperature variations.
- Relative humidity percentages.
- Gradual battery degradation trends.

The calculation engine separates the pipeline execution into two chronological layers:

- **Hourly Rolling Streams:** Groups observations into 1-hour intervals to calculate a moving average of the immediate, preceding hours.
- **Daily Rolling Baselines:** Groups observations into 1-day intervals to calculate a broader, preceding daily baseline.

The first rows in each partitioned sensor window will return empty or null values until the historical record count matches the required window size.


## Results

Hourly and Daily Average of Sensor readings.

| sensor_id | hourly_window | daily_window | hourly_avg_temp | daily_avg_temp | hourly_avg_humidity | daily_avg_humidity | hourly_avg_battery | daily_avg_battery |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SENS-01 | 2026-01-01T05:00:00.000000+0000 | 2026-01-01 | -2.2 | 16.48 | 25.0 | 53.5 | 99.1 | 95.62 |
| SENS-01 | 2026-01-01T07:00:00.000000+0000 | 2026-01-01 | 30.8 | 16.48 | 90.0 | 53.5 | 97.5 | 95.62 |
| SENS-01 | 2026-01-01T13:00:00.000000+0000 | 2026-01-01 | 2.6 | 16.48 | 76.0 | 53.5 | 94.6 | 95.62 |
| SENS-01 | 2026-01-01T14:00:00.000000+0000 | 2026-01-01 | 34.7 | 16.48 | 23.0 | 53.5 | 91.3 | 95.62 |
| SENS-01 | 2026-01-02T01:00:00.000000+0000 | 2026-01-02 | 2.8 | 25.07 | 51.0 | 57.8 | 85.9 | 83.15 |
| SENS-01 | 2026-01-02T06:00:00.000000+0000 | 2026-01-02 | 38.4 | 25.07 | 37.0 | 57.8 | 87.3 | 83.15 |
| SENS-01 | 2026-01-02T11:00:00.000000+0000 | 2026-01-02 | 27.8 | 25.07 | 89.0 | 57.8 | 82.0 | 83.15 |
| SENS-01 | 2026-01-02T12:00:00.000000+0000 | 2026-01-02 | 30.0 | 25.07 | 54.0 | 57.8 | 83.7 | 83.15 |
| SENS-01 | 2026-01-02T13:00:00.000000+0000 | 2026-01-02 | 41.9 | 25.07 | 47.0 | 57.8 | 81.6 | 83.15 |

[View Rolling Monitoring Results](https://github.com/itsanibose/cintel-04-sensor-monitoring/blob/main/artifacts/sensor_metrics.csv)

## Interpretation

The resampled metrics reveal distinct periods of environmental variation,
stabilized stabilization windows, and shifting system operational metrics.

Across the observation history, localized temperature and humidity readings
fluctuate alongside a linear reduction in device battery levels.

This structured breakdown helps distinguish expected, continuous resource
consumption patterns from sudden, sharp deviations in environmental conditions across distinct sensor deployments.

## Limitations

Time-series resampling effectively filters out erratic hourly data spikes,
but large aggregation windows may obscure short-term, micro-level sensor anomalies.

The current implementation utilizes fixed hourly and daily window configurations.
Alternative grouping intervals may capture different variations in device activity profiles.

The analytical engine evaluates static constraints and aggregations, but does not yet
include dynamic thresholding, machine learning models, or live alert notifications.

## Conclusion

Resampling high-frequency sensor intervals adds a clear chronological perspective to complex time-series data streams.

It establishes a structured foundation for tracking multi-device fleet performance, identifying hardware degradation trends,
and isolating faulty sensors for immediate inspection.

## Documentation Index

- **Home** - this landing page
- [**Project Instructions**](project-instructions.md)
- [**Glossary**](glossary.md)
- [**API**](api.md)
- [**Reactive App**](./app/index.html)

## Project Links

- [GitHub Repository](https://github.com/itsanibose/cintel-04-sensor-monitoring)
- [Example Pipeline](https://github.com/itsanibose/cintel-04-sensor-monitoring/blob/main/src/cintel/rolling_monitor.py)
- [Results and Artifacts](https://github.com/itsanibose/cintel-04-sensor-monitoring/tree/main/artifacts)

## Project Resources

- [Project Instructions](project-instructions.md)
- [Professional Python Guide](https://denisecase.github.io/pro-analytics-02/)
- [Professional Python Project Explainer](https://pup-pack.github.io/professional-python-project-explainer/).
- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)
