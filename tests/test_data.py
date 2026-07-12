import pandas as pd
import pytest

from src.data import load_events, load_price_data


def test_load_price_data_parses_mixed_date_formats(tmp_path):
    csv_path = tmp_path / "prices.csv"
    csv_path.write_text('Date,Price\n20-May-87,18.63\n"Apr 22, 2020",13.77\n')

    df = load_price_data(csv_path)

    assert list(df.columns) == ["Price"]
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.is_monotonic_increasing
    assert df.loc["1987-05-20", "Price"] == 18.63


def test_load_price_data_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_price_data(tmp_path / "does_not_exist.csv")


def test_load_price_data_missing_columns_raises(tmp_path):
    csv_path = tmp_path / "prices.csv"
    csv_path.write_text("Date,Close\n20-May-87,18.63\n")

    with pytest.raises(ValueError, match="missing columns"):
        load_price_data(csv_path)


def test_load_price_data_empty_file_raises(tmp_path):
    csv_path = tmp_path / "prices.csv"
    csv_path.write_text("Date,Price\n")

    with pytest.raises(ValueError, match="no rows"):
        load_price_data(csv_path)


def test_load_events_sorts_chronologically(tmp_path):
    csv_path = tmp_path / "events.csv"
    csv_path.write_text(
        "Date,Event,Category,Description,Expected_Direction\n"
        "2020-01-01,B,Conflict,desc,Increase\n"
        "1990-01-01,A,Conflict,desc,Decrease\n"
    )

    df = load_events(csv_path)

    assert list(df["Event"]) == ["A", "B"]


def test_load_events_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_events(tmp_path / "missing_events.csv")
