# brent-oil-price-analysis

Bayesian Change Point Analysis of Brent Oil Prices to identify structural breaks caused by geopolitical, economic, and OPEC-related events using PyMC, with an interactive Flask and React dashboard.

## Status

- **Task 1a — Foundation docs (complete):** analysis workflow, event dataset, assumptions/limitations.
- **Task 1b — EDA (complete):** trend, stationarity, volatility analysis, refactored into reusable `src/` modules.
- **Task 2 — Bayesian change point modeling:** in progress.
- **Task 3 — Interactive dashboard (Flask + React):** not started.

## Project Structure

```
├── data/
│   ├── raw/BrentOilPrices.csv   # daily Brent price, 20-May-1987 to 30-Sep-2022
│   ├── processed/               # generated plots and derived data
│   └── events.csv                # 21 researched geopolitical/OPEC/economic events (Task 1a)
├── docs/
│   ├── analysis_workflow.md              # end-to-end workflow, Task 1a deliverable
│   └── assumptions_and_limitations.md    # assumptions, limitations, correlation-vs-causation (Task 1a)
├── notebooks/
│   └── 01_eda.ipynb             # Task 1b EDA: trend, log returns, stationarity, volatility, events overlay
├── scripts/                     # standalone analysis scripts
├── src/                         # reusable library code
│   ├── data.py                  # load_price_data, load_events (with validation/error handling)
│   ├── preprocessing.py         # clip_date_range, add_log_returns, add_rolling_volatility
│   ├── stationarity.py          # adf_test, format_adf_result
│   └── plotting.py               # plot_price_series, plot_log_returns, plot_rolling_volatility, plot_price_with_events
├── tests/                       # pytest unit tests for src/ (17 tests, incl. error-path coverage)
└── requirements.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/01_eda.ipynb
```

## Running Tests

```bash
python3 -m pytest tests/ -v
```

## Key Documents

- [Analysis workflow](docs/analysis_workflow.md) — Task 1a deliverable: the full data-to-insight process, how the events dataset is used downstream in EDA and change point modeling, and how time series properties (trend, stationarity, volatility) inform the Bayesian change point model design.
- [Assumptions & limitations](docs/assumptions_and_limitations.md) — Task 1a deliverable: including the correlation-vs-causation distinction central to interpreting change point results.
- [Events dataset](data/events.csv) — Task 1a deliverable: 21 major supply/demand shocks (1990–2022) used to interpret detected change points.
