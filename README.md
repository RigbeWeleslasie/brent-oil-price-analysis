# brent-oil-price-analysis

Bayesian Change Point Analysis of Brent Oil Prices to identify structural breaks caused by geopolitical, economic, and OPEC-related events using PyMC, with an interactive Flask and React dashboard.

## Status

- **Task 1 — Foundation (complete):** analysis workflow, event dataset, assumptions/limitations, initial EDA.
- **Task 2 — Bayesian change point modeling:** in progress.
- **Task 3 — Interactive dashboard (Flask + React):** not started.

## Project Structure

```
├── data/
│   ├── raw/BrentOilPrices.csv   # daily Brent price, 20-May-1987 to 30-Sep-2022
│   ├── processed/               # generated plots and derived data
│   └── events.csv                # 21 researched geopolitical/OPEC/economic events
├── docs/
│   ├── analysis_workflow.md              # end-to-end workflow, task 1 deliverable
│   └── assumptions_and_limitations.md    # assumptions, limitations, correlation-vs-causation
├── notebooks/
│   └── 01_eda.ipynb             # EDA: trend, log returns, stationarity, volatility, events overlay
├── scripts/                     # standalone analysis scripts
├── src/                         # shared library code (data loading, modeling, dashboard backend)
├── tests/                       # unit tests
└── requirements.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/01_eda.ipynb
```

## Key Documents

- [Analysis workflow](docs/analysis_workflow.md) — the full data-to-insight process, including how time series properties (trend, stationarity, volatility) inform the Bayesian change point model design.
- [Assumptions & limitations](docs/assumptions_and_limitations.md) — including the correlation-vs-causation distinction central to interpreting change point results.
- [Events dataset](data/events.csv) — 21 major supply/demand shocks (1990–2022) used to interpret detected change points.
