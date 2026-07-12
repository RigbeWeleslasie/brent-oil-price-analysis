# Analysis Workflow: Change Point Analysis of Brent Oil Prices

*Task 1a deliverable — planned analysis steps, event data compilation, and*
*communication channels. Time series property analysis for Task 1b lives in*
*`notebooks/01_eda.ipynb`; see the summary in Section 2a and Step 3 below.*

## 1. Objective (Task 1a)

Quantify how major geopolitical, economic, and OPEC-policy events have shaped
structural shifts in Brent crude oil prices (daily, 20-May-1987 to
30-Sep-2022), and communicate those shifts in terms decision-makers
(investors, policymakers, energy companies) can act on.

## 2. Workflow Steps (Task 1a)

**Step 1 — Data ingestion and cleaning**
Load `data/raw/BrentOilPrices.csv`, parse `Date` (day-month-year, e.g.
`20-May-87`) to datetime, sort chronologically, check for gaps/duplicates and
missing values, and set `Date` as the index. Implemented in
`src/data.py::load_price_data`.

**Step 2 — Event data compilation (Task 1a deliverable: `data/events.csv`)**
Research and tabulate 10-15+ major supply/demand shocks: OPEC(+) decisions,
wars and civil conflicts in producing regions, sanctions, and macroeconomic
shocks. Loaded via `src/data.py::load_events`. These serve as candidate
explanations to compare against statistically detected change points — they
are not fed into the change point model itself.

### 2a. Events Dataset — How It Is Used Downstream

`data/events.csv` is not a model input; it is a reference table consulted at
two later stages:

- **EDA (Task 1b, `notebooks/01_eda.ipynb`)**: event dates are plotted as
  vertical markers over the price series (`src/plotting.py::plot_price_with_events`)
  and checked against spikes in rolling volatility — a first, purely
  descriptive look at whether known events line up with visible turbulence.
- **Change point modeling (Task 2)**: once the Bayesian model produces a
  posterior distribution for the switch point `tau`, its credible interval is
  compared against the dates in `data/events.csv` (Step 6 below) to formulate
  — not prove — a hypothesis about which event most plausibly triggered each
  detected shift.

**Step 3 — Exploratory Data Analysis (Task 1b, EDA)**
- Plot the raw price series to spot visible trends, shocks, and volatility
  regimes.
- Compute log returns, `r_t = log(P_t) - log(P_{t-1})`, since raw prices are
  non-stationary (trending, changing variance) and are not well suited to
  standard time series or change point models.
- Test stationarity of price levels vs. log returns (Augmented Dickey-Fuller).
- Inspect rolling volatility / squared returns for volatility clustering
  (periods of turbulence following each other), which motivates why a
  single-regime constant-variance model is inadequate.

**Step 4 — Bayesian change point modeling (PyMC)**
- Model log returns (or a segment of the price series) with a discrete
  switch point `tau` (uniform prior over time indices).
- Define pre-/post-change parameters (e.g., `mu_1`, `mu_2`, and optionally
  `sigma_1`, `sigma_2`).
- Use `pm.math.switch` to route each time index to the correct regime
  parameters, and connect to the data via a `pm.Normal` likelihood.
- Sample the posterior with `pm.sample()` (NUTS/Metropolis as appropriate for
  the discrete `tau`).
- For the full 35-year series, consider iterating the model over shorter
  windows around candidate events, since a single switch point cannot capture
  the many regimes present across three and a half decades.

**Step 5 — Model diagnostics and interpretation**
- Check convergence: `pm.summary()` (r_hat ~ 1.0, adequate effective sample
  size), `pm.plot_trace()` for mixing.
- Plot the posterior of `tau` — a narrow peak indicates a confidently
  localized change point; a diffuse posterior indicates ambiguity (possibly
  several smaller shifts rather than one large one).
- Summarize posterior distributions of before/after parameters and compute
  probabilistic statements, e.g. `P(mu_2 > mu_1)`, credible intervals for the
  size of the shift.

**Step 6 — Associating change points with events**
- Compare the credible interval of each detected `tau` against
  `data/events.csv` dates.
- Formulate hypotheses for the most plausible triggering event(s), favoring
  temporal proximity and consistency of direction (e.g., a downward shift
  aligning with an OPEC decision not to cut output).
- Quantify: "Following event X (date), the model places a change point at
  [date range]; the mean daily price shifts from $A to $B (a change of C%),
  with posterior probability P that the shift is an increase/decrease."

**Step 7 — Communication**
- Package findings as a written report (blog-post style) with annotated
  price/return plots, posterior plots, and quantified impact statements.
- Build the interactive dashboard (Flask API + React frontend) so
  stakeholders can explore the price series, filter by date range, and toggle
  event overlays themselves.

## 3. Communication Channels

- **Written report**: Medium-style blog post / PDF for external stakeholders
  (investors, policymakers) — narrative + key visualizations.
- **Interactive dashboard**: Flask + React app for analysts who want to
  explore the data and change points directly.
- **Jupyter notebooks**: technical audience (internal team, tutors) —
  full reproducible analysis.
- **GitHub repository**: code, data, and issue tracking for collaboration
  and version history.

## 4. Correlation vs. Causation — Why This Matters Here

A Bayesian change point model identifies *when* the statistical properties of
the price series (mean, variance) shifted — it does not, by itself, prove
*why*. Associating a detected change point with a nearby event in
`data/events.csv` is an inference of plausibility based on temporal
proximity and domain knowledge, not a causal test. Key reasons this
distinction matters:

- **Confounding and coincidence**: Multiple events often cluster in time
  (e.g., 2020 combined a Saudi-Russia price war with the COVID-19 demand
  shock); a single change point cannot be cleanly attributed to one cause.
- **Anticipation effects**: Markets are forward-looking, so prices often move
  *before* the official event date (e.g., ahead of a scheduled OPEC meeting)
  as traders price in expectations, which can shift the estimated `tau` away
  from the "true" trigger date.
- **No counterfactual**: We do not observe what oil prices *would have been*
  absent the event, so we cannot rigorously isolate its causal effect size —
  we can only describe the size of the observed shift.
- **Direction of inference**: We are matching detected structural breaks to a
  pre-researched list of known events (event-informed hypothesis generation),
  not testing whether events *cause* breaks in a designed, controlled sense.

Given this, all "impact" statements in this analysis are phrased as
observed associations ("a change point coincides with X, consistent with the
hypothesis that X contributed to the shift"), not causal claims.
