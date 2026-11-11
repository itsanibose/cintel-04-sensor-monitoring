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
- Source: [sample sensor

[View Example Dataset](https://github.com/itsanibose/cintel-04-sensor-monitoring/blob/main/data/sample-sensors.csv)

## Methods

The pipeline sorts observations by timestamp
and computes rolling averages using a window
of three observations.

Rolling averages are calculated for:

- Requests.
- Errors.
- Total latency.

Each completed window summarizes the current
observation and the two preceding observations.

The first two rows have no rolling average
because the full window is not yet available.

## Results

The rolling metrics show several changes in activity.

| Time  | Rolling Requests | Rolling Errors |
| ----- | ---------------: | -------------: |
| 08:10 |           135.00 |           3.00 |
| 08:25 |           171.67 |           6.00 |
| 08:50 |           145.00 |           2.33 |
| 09:10 |           198.33 |           7.67 |

[View Rolling Monitoring Results](https://github.com/denisecase/cintel-04-rolling-monitoring/blob/main/artifacts/rolling_metrics.csv)

## Interpretation

The rolling averages reveal periods of increasing
activity, declining activity, and renewed growth.

Toward the end of the observation period,
request counts and error counts both increase.

This suggests that growing workload may coincide
with additional errors, although the data
does not establish a causal relationship.

## Limitations

Rolling averages smooth short-term variation,
but may delay detection of sudden changes.

The example uses a fixed three-observation window.
Different window sizes may reveal different patterns.

The pipeline does not yet classify anomalies
or issue monitoring alerts.

## Conclusion

Rolling monitoring adds a temporal perspective
to system analysis.

It provides a foundation for identifying developing
patterns and determining when further investigation
may be useful.

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
