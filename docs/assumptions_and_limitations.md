# Assumptions and Limitations

## Assumptions

1. **Daily closing price is representative.** The dataset records a single
   daily Brent price; intraday volatility, bid-ask spreads, and trading
   volume are not captured.
2. **Log returns are approximately stationary and normally distributed**
   for modeling purposes. In practice, financial returns exhibit fatter
   tails than the Normal distribution (excess kurtosis); we treat Normal
   likelihoods as a reasonable first approximation, not a perfect fit.
3. **A single switch point per model run is a simplification.** Real
   history contains many regime shifts; we either analyze windows around
   candidate events or acknowledge that a single-`tau` model only detects
   the *most dominant* shift within the analyzed range.
4. **Event dates are approximate "start" dates.** Many events (wars,
   sanctions regimes, OPEC policy shifts) unfold over weeks or months;
   the recorded date marks a reasonable anchor point (e.g., invasion date,
   meeting date, implementation day) rather than the full duration of
   impact.
5. **Markets are assumed efficient enough that news is priced in quickly**,
   but not perfectly instantaneously — this justifies looking for change
   points near, not necessarily exactly on, event dates.
6. **No missing-data imputation beyond forward-fill/drop.** Non-trading
   days (weekends, holidays) are simply absent from the series rather than
   interpolated.

## Limitations

1. **Correlation, not causation.** As detailed in
   `docs/analysis_workflow.md`, matching a detected change point to an
   event is an inference of plausibility, not a proof of causal effect.
   Confounded, overlapping, or anticipated events make attribution
   inherently uncertain.
2. **Single time series, no macroeconomic controls.** The core model uses
   price/returns alone. It does not control for concurrent macro variables
   (USD strength, global GDP growth, inventories, interest rates) that also
   move oil prices — see "Future Work" for extensions (VAR, exogenous
   regressors).
3. **Event list is not exhaustive.** `data/events.csv` covers major,
   well-documented events but omits many smaller supply/demand shifts,
   weather disruptions, and regional conflicts that may also explain
   minor change points.
4. **Discrete uniform prior on tau assumes no prior belief about when
   changes occur.** This is a deliberately uninformative choice; using
   event dates to inform the prior would improve precision but also
   risks circular reasoning (finding what we told the model to look for).
5. **Model comparison and validation are limited.** With one dominant
   change point per run, we do not exhaustively test alternative numbers
   of change points (e.g., via reversible-jump MCMC or explicit model
   comparison) in the core deliverable; this is noted as an extension.
6. **Survivorship of data source.** The provided CSV is the sole price
   source; no cross-validation against an independent price feed
   (e.g., ICE Brent futures settlement) is performed.

## How This Shapes Modeling Choices

- Use **log returns**, not raw prices, as the primary series for the change
  point model, since raw prices are non-stationary (trending) while log
  returns are closer to stationary and better satisfy the constant-mean/
  constant-variance-within-regime assumption of the switch-point model.
- Treat detected change points as **hypotheses to be checked against
  domain knowledge** (the events table), not as confirmed causal findings.
- Present quantified impacts with **credible intervals and posterior
  probabilities**, not single point estimates, to reflect genuine
  uncertainty in both the timing and magnitude of shifts.
