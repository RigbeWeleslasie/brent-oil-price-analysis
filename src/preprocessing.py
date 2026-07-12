"""Cleaning and feature derivation for the Brent price series (Task 1b EDA)."""

import numpy as np
import pandas as pd


def clip_date_range(df: pd.DataFrame, end_date: str) -> pd.DataFrame:
    """Drop rows dated after ``end_date``.

    Used to clip the raw file (which runs a few weeks past 30-Sep-2022) back
    to the date range documented in the project brief.

    Parameters
    ----------
    df : pd.DataFrame
        Datetime-indexed DataFrame.
    end_date : str
        Inclusive upper bound, e.g. ``"2022-09-30"``.

    Raises
    ------
    ValueError
        If ``df`` is not datetime-indexed.
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("clip_date_range requires a DatetimeIndex")
    return df[df.index <= end_date]


def add_log_returns(df: pd.DataFrame, price_col: str = "Price") -> pd.DataFrame:
    """Add ``log_price`` and ``log_return`` columns, dropping the first NaN row.

    ``log_return`` is defined as ``log(P_t) - log(P_{t-1})``, the standard
    stationary transform for a trending, heteroskedastic price series.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``price_col`` with strictly positive values.
    price_col : str, default "Price"
        Name of the price column to transform.

    Raises
    ------
    ValueError
        If ``price_col`` is missing or contains non-positive values.
    """
    if price_col not in df.columns:
        raise ValueError(f"Column '{price_col}' not found in DataFrame")
    if (df[price_col] <= 0).any():
        raise ValueError(f"Column '{price_col}' must be strictly positive to take logs")

    out = df.copy()
    out["log_price"] = np.log(out[price_col])
    out["log_return"] = out["log_price"].diff()
    return out.dropna(subset=["log_return"])


def add_rolling_volatility(df: pd.DataFrame, column: str = "log_return", window: int = 30) -> pd.DataFrame:
    """Add a rolling standard deviation column named ``rolling_vol``.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain ``column``.
    column : str, default "log_return"
        Column to compute rolling volatility on.
    window : int, default 30
        Rolling window size in trading days.

    Raises
    ------
    ValueError
        If ``column`` is missing or ``window`` is not a positive integer.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    if window <= 0:
        raise ValueError("window must be a positive integer")

    out = df.copy()
    out["rolling_vol"] = out[column].rolling(window).std()
    return out
