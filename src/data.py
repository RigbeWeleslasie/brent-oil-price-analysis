"""Loading and validating raw Brent price and event data (Task 1a/1b)."""

from pathlib import Path

import pandas as pd

PRICE_COLUMNS = {"Date", "Price"}
EVENT_COLUMNS = {"Date", "Event", "Category", "Description", "Expected_Direction"}


def load_price_data(path: str | Path) -> pd.DataFrame:
    """Load the raw Brent price CSV into a datetime-indexed DataFrame.

    The source file mixes two date formats (``20-May-87`` and
    ``Apr 22, 2020``), so dates are parsed with ``format="mixed"``.

    Parameters
    ----------
    path : str | Path
        Path to a CSV with ``Date`` and ``Price`` columns.

    Returns
    -------
    pd.DataFrame
        Sorted, datetime-indexed DataFrame with a single ``Price`` column.

    Raises
    ------
    FileNotFoundError
        If ``path`` does not exist.
    ValueError
        If required columns are missing or the file contains no rows.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Price data file not found: {path}")

    df = pd.read_csv(path)
    missing = PRICE_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Price data at {path} is missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError(f"Price data at {path} contains no rows")

    df["Date"] = pd.to_datetime(df["Date"], format="mixed")
    df = df.sort_values("Date").reset_index(drop=True).set_index("Date")
    return df[["Price"]]


def load_events(path: str | Path) -> pd.DataFrame:
    """Load the researched events dataset (Task 1a deliverable).

    Parameters
    ----------
    path : str | Path
        Path to a CSV with columns: Date, Event, Category, Description,
        Expected_Direction.

    Returns
    -------
    pd.DataFrame
        Datetime-indexed events, sorted chronologically.

    Raises
    ------
    FileNotFoundError
        If ``path`` does not exist.
    ValueError
        If required columns are missing or the file contains no rows.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Events data file not found: {path}")

    df = pd.read_csv(path)
    missing = EVENT_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Events data at {path} is missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError(f"Events data at {path} contains no rows")

    df["Date"] = pd.to_datetime(df["Date"])
    return df.sort_values("Date").reset_index(drop=True)
