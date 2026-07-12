"""Reusable EDA plotting helpers for the Brent price series (Task 1b)."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

EXPECTED_DIRECTION_COLORS = {"Increase": "#c0392b", "Decrease": "#27ae60"}


def _save_if_requested(fig: plt.Figure, save_path: str | Path | None) -> None:
    if save_path is not None:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=120)


def plot_price_series(
    df: pd.DataFrame,
    price_col: str = "Price",
    title: str = "Brent Crude Oil Price",
    save_path: str | Path | None = None,
) -> plt.Axes:
    """Plot a price (or any single-column) series over time.

    Raises
    ------
    ValueError
        If ``price_col`` is missing or ``df`` is empty.
    """
    if price_col not in df.columns:
        raise ValueError(f"Column '{price_col}' not found in DataFrame")
    if df.empty:
        raise ValueError("Cannot plot an empty DataFrame")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df[price_col], linewidth=0.8, color="#1f5c8a")
    ax.set_title(title)
    ax.set_ylabel("USD per barrel")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    _save_if_requested(fig, save_path)
    return ax


def plot_log_returns(
    df: pd.DataFrame,
    column: str = "log_return",
    title: str = "Brent Daily Log Returns",
    save_path: str | Path | None = None,
) -> plt.Axes:
    """Plot log returns over time.

    Raises
    ------
    ValueError
        If ``column`` is missing or ``df`` is empty.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    if df.empty:
        raise ValueError("Cannot plot an empty DataFrame")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df[column], linewidth=0.5, color="#c0392b")
    ax.set_title(title)
    ax.set_ylabel("log(P_t) - log(P_{t-1})")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    _save_if_requested(fig, save_path)
    return ax


def plot_rolling_volatility(
    df: pd.DataFrame,
    column: str = "rolling_vol",
    window: int = 30,
    save_path: str | Path | None = None,
) -> plt.Axes:
    """Plot a precomputed rolling volatility column over time.

    Raises
    ------
    ValueError
        If ``column`` is missing or ``df`` is empty.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    if df.empty:
        raise ValueError("Cannot plot an empty DataFrame")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df[column], linewidth=0.8, color="#8e44ad")
    ax.set_title(f"{window}-Day Rolling Volatility of Log Returns")
    ax.set_ylabel("Rolling std. dev. of log returns")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    _save_if_requested(fig, save_path)
    return ax


def plot_price_with_events(
    df: pd.DataFrame,
    events: pd.DataFrame,
    price_col: str = "Price",
    save_path: str | Path | None = None,
) -> plt.Axes:
    """Plot the price series with vertical lines marking researched events.

    Events are colored by their ``Expected_Direction`` (Increase/Decrease)
    and clipped to the price series' date range before plotting.

    Raises
    ------
    ValueError
        If required columns are missing or either input is empty.
    """
    if price_col not in df.columns:
        raise ValueError(f"Column '{price_col}' not found in price DataFrame")
    if df.empty:
        raise ValueError("Cannot plot an empty price DataFrame")
    if "Date" not in events.columns and not isinstance(events.index, pd.DatetimeIndex):
        raise ValueError("events must have a 'Date' column or a DatetimeIndex")

    event_dates = events["Date"] if "Date" in events.columns else events.index
    directions = events["Expected_Direction"] if "Expected_Direction" in events.columns else None
    in_range = (event_dates >= df.index.min()) & (event_dates <= df.index.max())

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df[price_col], linewidth=0.8, color="#1f5c8a", zorder=1)
    for i, (date, keep) in enumerate(zip(event_dates, in_range)):
        if not keep:
            continue
        direction = directions.iloc[i] if directions is not None else None
        color = EXPECTED_DIRECTION_COLORS.get(direction, "gray")
        ax.axvline(date, color=color, alpha=0.35, linewidth=1)

    ax.set_title("Brent Price with Researched Events Overlaid (red=expected increase, green=expected decrease)")
    ax.set_ylabel("USD per barrel")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    _save_if_requested(fig, save_path)
    return ax
