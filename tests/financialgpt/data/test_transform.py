from financialgpt.data.transform import (
    normalize_target_allocation,
    normalize_column_names,
    normalize_client_allocation,
)
from pandas import DataFrame
import pandas as pd
import pytest


@pytest.fixture
def client_allocation() -> DataFrame:
    """
    Fixture to load a sample client allocation DataFrame for testing.

    Returns:
        DataFrame: A sample client allocation DataFrame.
    """
    return pd.read_csv("data/01_raw/financial_advisor_clients.csv")


@pytest.fixture
def target_allocation() -> DataFrame:
    """
    Fixture to load a sample target allocation DataFrame for testing.

    Returns:
        DataFrame: A sample target allocation DataFrame.
    """
    return pd.read_csv("data/01_raw/client_target_allocations.csv")


def test_normalize_column_names() -> None:
    """
    Test the normalize_column_names function.
    """
    df = pd.DataFrame(
        {
            "Column Name": [1, 2, 3],
            "Col-Name": [4, 5, 6],
            "Column/Name": [7, 8, 9],
            "Column (%)": [10, 11, 12],
            "52-Week High": [13, 14, 15],
        }
    )

    expected_columns = [
        "column_name",
        "col_name",
        "columnname",
        "column_percent",
        "week_52_high",
    ]

    normalized_df = normalize_column_names(df)

    assert normalized_df.columns.tolist() == expected_columns
    assert not normalized_df.columns.duplicated().any()


def test_normalized_client_allocation(client_allocation: DataFrame) -> None:
    """
    Test the normalized client_allocation.

    Args:
        client_allocation (DataFrame): The sample client allocation DataFrame.
    """
    client_allocation, _ = normalize_client_allocation(client_allocation)

    assert all(client_allocation["client"].str.match(r"^Client_\d+$"))

    assert not client_allocation[["client", "symbol", "quantity"]].isnull().any().any()

    assert client_allocation["symbol"].str.isupper().all()

    assert client_allocation["quantity"].dtype == float


def test_normalized_asset_performance(client_allocation: DataFrame) -> None:
    """
    Test the normalized asset_performance.

    Args:
        client_allocation (DataFrame): The sample client allocation DataFrame.
    """
    _, asset_performance = normalize_client_allocation(client_allocation)

    assert not asset_performance.isnull().values.any()

    # Check if the 'sector' column values are within the specified list
    valid_sectors = [
        "ETF",
        "Communication Services",
        "Consumer Discretionary",
        "Technology",
        "Consumer Staples",
        "Health Care",
        "Financials",
    ]
    assert asset_performance["sector"].isin(valid_sectors).all()

    assert not asset_performance.duplicated().any()


def test_normalized_target_allocation(target_allocation: DataFrame) -> None:
    """
    Test the normalized target_allocation.

    Args:
        target_allocation (DataFrame): The sample target allocation DataFrame.
    """
    target_allocation, _ = normalize_target_allocation(target_allocation)

    assert not target_allocation.isnull().values.any()

    assert all(target_allocation["client"].str.match(r"^Client_\d+$"))

    grouped = target_allocation.groupby("client")["target_allocation_percent"].sum()
    assert (grouped == 100).all()

    row_counts = target_allocation["client"].value_counts()
    assert (row_counts == 4).all()


def test_normalized_client_profile(target_allocation: DataFrame) -> None:
    """
    Test the normalized client_profile.

    Args:
        target_allocation (DataFrame): The sample target allocation DataFrame.
    """
    _, client_profile = normalize_target_allocation(target_allocation)

    assert not client_profile.isnull().values.any()

    assert all(client_profile["client"].str.match(r"^Client_\d+$"))

    valid_profiles = [
        "Aggressive Growth",
        "Growth",
        "Balanced",
        "Conservative",
    ]
    assert client_profile["target_portfolio"].isin(valid_profiles).all()
