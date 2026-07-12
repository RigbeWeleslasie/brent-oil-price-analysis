import numpy as np
import pandas as pd
import pytest

from src.stationarity import adf_test, format_adf_result


def test_adf_test_detects_stationary_white_noise():
    rng = np.random.default_rng(42)
    series = pd.Series(rng.normal(size=500))

    result = adf_test(series, label="white noise")

    assert result["is_stationary"] is True
    assert result["label"] == "white noise"
    assert "1%" in result["critical_values"]


def test_adf_test_detects_nonstationary_random_walk():
    rng = np.random.default_rng(42)
    series = pd.Series(rng.normal(size=500).cumsum())

    result = adf_test(series, label="random walk")

    assert result["is_stationary"] is False


def test_adf_test_rejects_too_short_series():
    with pytest.raises(ValueError, match="fewer than 2"):
        adf_test(pd.Series([1.0]), label="tiny")


def test_format_adf_result_includes_label_and_verdict():
    result = {
        "label": "log returns",
        "adf_statistic": -10.0,
        "p_value": 0.001,
        "critical_values": {"1%": -3.4, "5%": -2.9, "10%": -2.6},
        "is_stationary": True,
    }

    text = format_adf_result(result)

    assert "log returns" in text
    assert "stationary" in text
