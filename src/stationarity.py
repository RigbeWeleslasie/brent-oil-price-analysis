"""Stationarity testing helpers (Task 1b: informs the change point model design)."""

import pandas as pd
from statsmodels.tsa.stattools import adfuller


def adf_test(series: pd.Series, label: str, alpha: float = 0.05) -> dict:
    """Run an Augmented Dickey-Fuller test and summarize the result.

    Parameters
    ----------
    series : pd.Series
        Series to test (e.g. raw price level or log returns).
    label : str
        Human-readable name used in the returned summary.
    alpha : float, default 0.05
        Significance level for the stationarity verdict.

    Returns
    -------
    dict
        Keys: ``label``, ``adf_statistic``, ``p_value``, ``critical_values``,
        ``is_stationary``.

    Raises
    ------
    ValueError
        If ``series`` has fewer than 2 non-null observations.
    """
    clean = series.dropna()
    if len(clean) < 2:
        raise ValueError(f"Series '{label}' has fewer than 2 observations after dropping NaNs")

    statistic, p_value, _, _, critical_values, _ = adfuller(clean, autolag="AIC")
    return {
        "label": label,
        "adf_statistic": statistic,
        "p_value": p_value,
        "critical_values": critical_values,
        "is_stationary": bool(p_value < alpha),
    }


def format_adf_result(result: dict) -> str:
    """Render an `adf_test` result dict as a human-readable report string."""
    lines = [
        f"--- ADF test: {result['label']} ---",
        f"ADF statistic: {result['adf_statistic']:.4f}",
        f"p-value:       {result['p_value']:.4g}",
    ]
    lines += [f"critical value ({k}): {v:.4f}" for k, v in result["critical_values"].items()]
    conclusion = "stationary" if result["is_stationary"] else "non-stationary"
    lines.append(f"=> Series appears {conclusion} at the chosen significance level")
    return "\n".join(lines)
