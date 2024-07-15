from financialgpt.data.load import load_data, delete_existing_data
from financialgpt.data.transform import (
    normalize_target_allocation,
    normalize_client_allocation,
)
from financialgpt.entity import (
    ClientAllocation,
    ClientProfile,
    TargetAllocation,
    AssetPerformance,
)
import pandas as pd

target_allocation = pd.read_csv("data/01_raw/client_target_allocations.csv")
client_allocation = pd.read_csv("data/01_raw/financial_advisor_clients.csv")

client_allocation, asset_performance = normalize_client_allocation(client_allocation)
target_allocation, client_profile = normalize_target_allocation(target_allocation)

delete_existing_data()

load_data(client_profile, ClientProfile)
load_data(asset_performance, AssetPerformance)
load_data(client_allocation, ClientAllocation)
load_data(target_allocation, TargetAllocation)
