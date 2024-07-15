import numpy as np
import pandas as pd
from pandas import DataFrame


def normalize_target_allocation(
    target_allocation: DataFrame,
) -> tuple[DataFrame, DataFrame]:
    """
    Create target allocation and client profile DataFrames from the target allocation DataFrame.

    Args:
        target_allocation (DataFrame): The target allocation DataFrame.

    Returns:
        tuple[DataFrame, DataFrame]: A tuple containing the target allocation DataFrame and the client profile DataFrame.
    """
    target_allocation = target_allocation.iloc[:200]
    client_profile = (
        target_allocation.groupby(by=["Client", "Target Portfolio"])
        .count()
        .reset_index()[["Client", "Target Portfolio"]]
    )

    target_allocation = target_allocation.drop("Target Portfolio", axis=1)
    target_allocation["Client"] = [f"Client_{int(i / 4) + 1}" for i in range(50 * 4)]
    target_allocation["Asset Class"] = ["Stocks", "Bonds", "ETFs", "Cash"] * 50

    allocation_fill_df = (
        target_allocation.groupby(by="Client")
        .sum()
        .reset_index()[["Client", "Target Allocation (%)"]]
    )
    replacements = dict(
        zip(
            allocation_fill_df["Client"],
            100 - allocation_fill_df["Target Allocation (%)"],
        )
    )
    target_allocation["Target Allocation (%)"] = target_allocation[
        "Target Allocation (%)"
    ].fillna(target_allocation["Client"].map(replacements))

    target_allocation = normalize_column_names(target_allocation)
    client_profile = normalize_column_names(client_profile)

    return target_allocation, client_profile


def normalize_client_allocation(
    client_allocation: DataFrame,
) -> tuple[DataFrame, DataFrame]:
    """
    Normalize the client allocation DataFrame.

    Args:
        client_allocation (DataFrame): The client allocation DataFrame.

    Returns:
        tuple[DataFrame, DataFrame]: A tuple containing the normalized client allocation and
                                        asset performance DataFrames.
    """

    client_allocation = fix_client_ids(client_allocation)
    client_allocation = remove_duplicates(client_allocation)
    client_allocation = fill_na_values(client_allocation)

    asset_performance = get_asset_performance(client_allocation)
    client_allocation = get_client_allocation(client_allocation)

    asset_performance = normalize_column_names(asset_performance)
    client_allocation = normalize_column_names(client_allocation)

    return client_allocation, asset_performance


def fix_client_ids(client_allocation: DataFrame) -> DataFrame:
    """
    Fix misspelled client IDs by ensuring they follow the format 'Client_<numeric_id>'.

    Args:
        client_allocation (DataFrame): The client allocation DataFrame.

    Returns:
        DataFrame: The DataFrame with corrected client IDs.
    """
    client_allocation["Client"] = client_allocation["Client"].apply(
        lambda x: f"Client_{''.join([c for c in x if c.isnumeric()])}"
    )
    wrongly_filled_ids = (
        (client_allocation.index > 135)
        & (client_allocation.index < 747)
        & (client_allocation.Client.apply(len) == 8)
    )
    client_allocation.loc[wrongly_filled_ids, "Client"] = client_allocation.shift(
        -1
    ).loc[wrongly_filled_ids, "Client"]
    return client_allocation


def remove_duplicates(client_allocation: DataFrame) -> DataFrame:
    """
    Remove duplicate rows based on 'Client' and 'Symbol' columns.

    Args:
        client_allocation (DataFrame): The client allocation DataFrame.

    Returns:
        DataFrame: The DataFrame with duplicates removed.
    """
    return client_allocation.drop_duplicates(subset=["Client", "Symbol"])


def fill_na_values(client_allocation: DataFrame) -> DataFrame:
    """
    Fill NA values in various columns of the client allocation DataFrame.

    Args:
        client_allocation (DataFrame): The client allocation DataFrame.

    Returns:
        DataFrame: The DataFrame with NA values filled.
    """

    client_allocation.loc[:, "Symbol"] = fill_na_with_reference(
        client_allocation, "Symbol", "Name"
    )

    columns_to_replace = [
        "Name",
        "Sector",
        "P/E Ratio",
        "Dividend Yield",
        "52-Week High",
        "52-Week Low",
        "Analyst Rating",
        "Target Price",
        "Risk Level",
    ]
    for column_to_fix in columns_to_replace:
        client_allocation.loc[:, column_to_fix] = fill_na_with_reference(
            client_allocation, column_to_fix, "Symbol"
        )

    client_allocation.loc[:, "Quantity"] = client_allocation["Quantity"].fillna(
        client_allocation["Market Value"] / client_allocation["Current Price"]
    )
    client_allocation.loc[:, "Current Price"] = client_allocation[
        "Current Price"
    ].fillna(client_allocation["Market Value"] / client_allocation["Quantity"])
    client_allocation.loc[:, "Market Value"] = client_allocation["Market Value"].fillna(
        client_allocation["Current Price"] * client_allocation["Quantity"]
    )
    client_allocation.loc[:, "Buy Price"] = (
        client_allocation["Buy Price"].replace({np.nan: None}).astype(float)
    )

    client_allocation.loc[:, "Purchase Date"] = pd.to_datetime(
        client_allocation["Purchase Date"].replace({np.nan: None}), format="%m/%d/%y"
    ).dt.date
    return client_allocation


def fill_na_with_reference(
    df: DataFrame,
    column_to_replace: str,
    column_reference: str,
) -> DataFrame:
    """
    Fill NA values in a specified column using a reference column for mapping.

    Args:
        df (DataFrame): The DataFrame to update.
        column_to_replace (str): The column in which to fill NA values.
        column_reference (str): The reference column to use for mapping.
        reference_df (DataFrame): The DataFrame containing reference data for mapping.

    Returns:
        DataFrame: The DataFrame with NA values filled.
    """
    multi_index = df.groupby(by=[column_to_replace, column_reference]).count().index
    replacements = {name: symbol for symbol, name in multi_index}
    return df[column_to_replace].fillna(df[column_reference].map(replacements))


def get_asset_performance(client_allocation: DataFrame) -> DataFrame:
    """
    Extract columns that relates only with the stocks.

    Args:
        client_allocation (DataFrame): The client allocation DataFrame.

    Returns:
        DataFrame: A DataFrame containing asset performance information.
    """
    asset_performance = (
        client_allocation.loc[
            :,
            [
                "Symbol",
                "Name",
                "Sector",
                "Current Price",
                "Dividend Yield",
                "P/E Ratio",
                "52-Week High",
                "52-Week Low",
                "Analyst Rating",
                "Target Price",
                "Risk Level",
            ],
        ]
        .drop_duplicates(subset=["Symbol"])
        .drop_duplicates(subset=["Name"])
    )
    return asset_performance


def get_client_allocation(client_allocation: DataFrame) -> DataFrame:
    """
    Extract columns that relates with both asset and client from the client allocation DataFrame.

    Args:
        client_allocation (DataFrame): The client allocation DataFrame.

    Returns:
        DataFrame: A DataFrame containing client allocation information.
    """
    client_allocation = client_allocation.loc[
        :, ["Client", "Symbol", "Quantity", "Buy Price", "Purchase Date"]
    ]
    return client_allocation


def normalize_column_names(df: DataFrame) -> DataFrame:
    """
    Normalize the column names

    Args:
        df (DataFrame): The DataFrame to have the columns normalized

    Returns:
        DataFrame: DataFrame with column names normalized
    """
    df.columns = [
        c.lower()
        .replace("(%)", "percent")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "")
        .replace("52_week", "week_52")
        for c in df
    ]
    return df


if __name__ == "__main__":
    client_allocation = pd.read_csv("data/01_raw/client_target_allocations.csv")
    target_allocation = pd.read_csv("data/01_raw/financial_advisor_clients.csv")

    client_allocation, asset_performance = normalize_client_allocation(
        client_allocation
    )
    target_allocation, client_profile = normalize_target_allocation(target_allocation)

    client_allocation.to_csv("data/02_primary/client_allocation.csv", index=False)
    client_profile.to_csv("data/02_primary/client_profile.csv", index=False)
    target_allocation.to_csv("data/02_primary/target_allocation.csv", index=False)
    asset_performance.to_csv("data/02_primary/asset_performance.csv", index=False)
