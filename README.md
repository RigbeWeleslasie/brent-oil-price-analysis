# brent-oil-price-analysis

Bayesian Change Point Analysis of Brent Oil Prices to identify structural breaks caused by geopolitical, economic, and OPEC-related events using PyMC, with an interactive Flask and React dashboard.

## Status

- **Task 1a — Foundation docs (complete):** analysis workflow, event dataset, assumptions/limitations.
- **Task 1b — EDA (complete):** trend, stationarity, volatility analysis, refactored into reusable `src/` modules.
- **Task 2 — Bayesian change point modeling (complete):** single and two-change-point models implemented with quantified impacts.
- **Task 3 — Interactive dashboard (Flask + React):** in progress.

## Key Findings

### Single Change Point Model
- **Detected Change Point:** February 23, 2005 (day index 4520)
- **Before:** Mean price of **$21.42/barrel** (95% HDI: $20.92 – $21.96)
- **After:** Mean price of **$75.61/barrel** (95% HDI: $75.07 – $76.12)
- **Impact:** ~253% increase in baseline oil prices
- **Model Diagnostics:** All parameters achieved R-hat (r̂) ≤ 1.01, confirming excellent MCMC convergence

### Advanced Two Change Point Model
The advanced model identified **three distinct market regimes**:

1. **Regime 1 (Pre-February 2004):** Mean = **$20.28/barrel** (95% HDI: $19.74 – $20.82)
   - Era of cheap, stable oil prices
2. **Regime 2 (Feb 2004 – Jul 2005):** Mean = **$44.10/barrel** (95% HDI: $41.85 – $46.12)
   - ~117% increase as global demand surged
   - Associated with the aftermath of the Iraq War (March 2003) and rapid industrialization in China/India
3. **Regime 3 (Post-July 2005):** Mean = **$76.19/barrel** (95% HDI: $75.65 – $76.70)
   - ~72% jump reflecting a permanently higher baseline
   - Market lost spare capacity, setting the stage for the 2008 peak

**Model Diagnostics:** All parameters achieved R-hat (r̂) ≤ 1.01 with effective sample sizes > 1000.

## Project Structure

```text
├── data/
│   ├── raw/
│   │   ├── BrentOilPrices.csv   # daily Brent price, 20-May-1987 to 30-Sep-2022
│   │   └── events.csv           # 21 researched geopolitical/OPEC/economic events (Task 1a)
│   └── processed/               # generated plots and derived data
├── docs/
│   ├── analysis_workflow.md              # end-to-end workflow, Task 1a deliverable
│   └── assumptions_and_limitations.md    # assumptions, limitations, correlation-vs-causation (Task 1a)
├── notebooks/
│   ├── 01_eda.ipynb                      # Task 1b EDA: trend, log returns, stationarity, volatility, events overlay
│   └── 02_change_point_model.ipynb       # Task 2: Interactive Bayesian modeling
├── scripts/                              # standalone analysis scripts
├── src/                                  # reusable library code
│   ├── data.py                           # load_price_data, load_events (with validation/error handling)
│   ├── preprocessing.py                  # clip_date_range, add_log_returns, add_rolling_volatility
│   ├── stationarity.py                   # adf_test, format_adf_result
│   ├── plotting.py                       # plot_price_series, plot_log_returns, plot_rolling_volatility, plot_price_with_events
│   ├── change_point_model.py             # Task 2: Single change point Bayesian model
│   └── two_change_point_model.py         # Task 2: Advanced two change point model (three regimes)
├── tests/                                # pytest unit tests for src/ (17 tests, incl. error-path coverage)
├── trace_plot.png                        # MCMC convergence diagnostics (single CP model)
├── posterior_tau.png                     # Change point posterior distribution (single CP model)
├── two_cp_trace_plot.png                 # MCMC convergence diagnostics (two CP model)
├── two_cp_posterior_taus.png             # Both change point posterior distributions
└── requirements.txt
