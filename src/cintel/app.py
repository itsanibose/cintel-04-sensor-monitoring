"""app.py - Reactive marimo app for this project.

Marimo adds reactive controls.
Every function below is a marimo cell.

RUN LOCALLY:

  uv run marimo edit src/cintel/app.py     # edit
  uv run marimo run  src/cintel/app.py     # run as an app (CTRL+c quits)

WASM DEPENDENCIES:

Under WebAssembly (emscripten) the browser has no project environment.
This app uses polars in addition to marimo, so the first cell installs
polars with micropip when running under WASM.

NO LOGGING:

A browser-based WASM app has no persistent Python server to store log files,
so this notebook configures no logging.

PLAN CELLS FIRST

1. Imports (installs WASM deps, returns shared imports and constants)
2. Opening title and introduction (Markdown)
3. Load and sort the IoT sensor time-series data (same cell handles local
   and WASM environments, via cintel.utils_system)
4. Compute hourly and daily averages (same logic as the CLI pipeline)
5. Sensor selection control (dropdown)
6. Filter and show the sensor metrics table
7. Closing (Markdown)

Note: marimo triggers @app.cell functions automatically; we never call them.
The names starting with "_" are for our own organization; the engine ignores
them.
"""

# === ONLY THIS AT THE TOP OF THE FILE ===

import marimo

__generated_with = "0.25.0"

app = marimo.App(width="medium")

# === FIRST CELL IMPORTS AND RETURNS DEPENDENCIES TO MAKE IT SELF-CONTAINED ===


@app.cell
async def _():
    import sys

    if sys.platform == "emscripten":
        import micropip

        await micropip.install("polars")

    import marimo as mo
    import polars as pl

    from cintel.utils_system import (
        compute_rolling_metrics_iot,
        load_timeseries_metrics,
    )

    return compute_rolling_metrics_iot, load_timeseries_metrics, mo, pl, sys


# === TITLE AND INTRODUCTION ===


@app.cell
def _(mo):
    mo.md(r"""
    # Rolling Monitoring: IoT Sensors

    IoT sensors report temperature, humidity, and battery level every
    15 minutes. A single reading can be noisy, so the pipeline rolls the
    readings up into **hourly** and **daily** averages per sensor.
    Comparing the two shows how each hour deviates from that day's baseline.
    Pick a sensor below to focus on one device, or view the whole fleet.
    """)


# === LOAD AND SORT THE TIME-SERIES DATA ===


@app.cell
def _(load_timeseries_metrics, mo, sys):
    """Load the IoT sensor time-series data. Two environments, one cell.

    Locally, polars reads the CSV from data/.
    Under WASM (emscripten), Pyodide's open_url() fetches the CSV from
    public/ and load_timeseries_metrics() reads and sorts it from there
    instead.
    """
    notebook_location = mo.notebook_location()

    if notebook_location is None:
        raise RuntimeError("Unable to determine notebook location.")

    filename = "sample-sensors.csv"

    if sys.platform == "emscripten":
        from pyodide.http import open_url  # ty: ignore[unresolved-import]

        data_url = notebook_location / "public" / filename
        df = load_timeseries_metrics(open_url(str(data_url)))
    else:
        data_path = notebook_location.parents[1] / "data" / filename
        df = load_timeseries_metrics(data_path)

    return (df,)


# === COMPUTE HOURLY AND DAILY AVERAGES (SAME LOGIC AS THE CLI PIPELINE) ===


@app.cell
def _(compute_rolling_metrics_iot, df):
    # Windows are fixed (1 hour and 1 calendar day), so no window size input.
    df_with_rolling = compute_rolling_metrics_iot(df)
    return (df_with_rolling,)


# === SENSOR SELECTION CONTROL ===


@app.cell
def _(df_with_rolling, mo):
    ALL_SENSORS = "All sensors"
    sensor_ids = sorted(df_with_rolling["sensor_id"].unique().to_list())
    sensor_choice = mo.ui.dropdown(
        options=[ALL_SENSORS, *sensor_ids],
        value=ALL_SENSORS,
        label="Sensor",
    )
    sensor_choice  # noqa: B018 (marimo often uses standalone expressions)
    return ALL_SENSORS, sensor_choice


# === FILTER AND SHOW THE SENSOR METRICS TABLE ===


@app.cell
def _(ALL_SENSORS, df_with_rolling, mo, pl, sensor_choice):
    if sensor_choice.value == ALL_SENSORS:
        df_view = df_with_rolling
    else:
        df_view = df_with_rolling.filter(pl.col("sensor_id") == sensor_choice.value)

    mo.vstack(
        [
            mo.md(f"**{df_view.height}** hourly rows for **{sensor_choice.value}**"),
            mo.ui.table(df_view),
        ]
    )


# === TYPICALLY END WITH A MARKDOWN SOURCE LINK AND CLOSING ===


@app.cell
def _(mo):
    mo.md(r"""
    ---
    [😊 Learn more at marimo.io](https://marimo.io/)
    ---

    **Running locally?**
    To stop the app, click in the VS Code terminal,
    then press **CTRL** and **c** together (CTRL+c).
    When it asks "Are you sure you want to quit? (y/N)",
    type **y** and press **Enter**.
    ---
    """)


if __name__ == "__main__":
    app.run()
