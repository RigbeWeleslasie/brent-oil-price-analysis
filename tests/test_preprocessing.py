import numpy as np
import pandas as pd
import pytest

from src.preprocessing import add_log_returns, add_rolling_volatility, clip_date_range


def _price_df():
    dates = pd.date_range("2020-01-01", periods=5, freq="D")
    return pd.DataFrame({"Price": [10.0, 11.0, 9.0, 12.0, 12.0]}, index=dates)


def test_clip_date_range_drops_rows_after_cutoff():
    df = _price_df()

    clipped = clip_date_range(df, "2020-01-03")

    assert clipped.index.max() == pd.Timestamp("2020-01-03")
    assert len(clipped) == 3


def test_clip_date_range_requires_datetime_index():
    df = pd.DataFrame({"Price": [1, 2, 3]})

    with pytest.raises(ValueError, match="DatetimeIndex"):
        clip_date_range(df, "2020-01-01")


def test_add_log_returns_matches_manual_calculation():
    df = _price_df()

    out = add_log_returns(df)

    expected_second_return = np.log(11.0) - np.log(10.0)
    assert len(out) == len(df) - 1  # first row dropped (NaN return)
    assert out["log_return"].iloc[0] == pytest.approx(expected_second_return)


def test_add_log_returns_rejects_non_positive_prices():
    df = pd.DataFrame({"Price": [10.0, -1.0, 5.0]})

    with pytest.raises(ValueError, match="strictly positive"):
        add_log_returns(df)


def test_add_log_returns_missing_column_raises():
    df = pd.DataFrame({"Close": [10.0, 11.0]})

    with pytest.raises(ValueError, match="not found"):
        add_log_returns(df)


def test_add_rolling_volatility_computes_std():
    df = pd.DataFrame({"log_return": [0.1, 0.2, 0.1, 0.3, 0.2]})

    out = add_rolling_volatility(df, window=2)

    assert out["rolling_vol"].iloc[1] == pytest.approx(df["log_return"].iloc[:2].std())


def test_add_rolling_volatility_rejects_non_positive_window():
    df = pd.DataFrame({"log_return": [0.1, 0.2]})

    with pytest.raises(ValueError, match="positive integer"):
        add_rolling_volatility(df, window=0)
