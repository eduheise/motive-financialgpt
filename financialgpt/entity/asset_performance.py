from sqlalchemy import Column, String, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AssetPerformance(Base):
    """
    SQLAlchemy ORM model for the 'asset_performance' table.

    Attributes:
        symbol (str): The unique symbol of the asset (primary key).
        name (str): The name of the asset.
        sector (str): The sector to which the asset belongs.
        current_price (decimal): The current price of the asset.
        dividend_yield (decimal): The dividend yield of the asset.
        pe_ratio (decimal): The price-to-earnings ratio of the asset.
        week_52_high (decimal): The 52-week high price of the asset.
        week_52_low (decimal): The 52-week low price of the asset.
        analyst_rating (str): The analyst rating for the asset.
        target_price (decimal): The target price of the asset.
        risk_level (str): The risk level of the asset.
    """

    __tablename__ = "asset_performance"

    symbol = Column(String(50), primary_key=True)
    name = Column(String(100))
    sector = Column(String(100))
    current_price = Column(DECIMAL(18, 2))
    dividend_yield = Column(DECIMAL(5, 2))
    pe_ratio = Column(DECIMAL(10, 2))
    week_52_high = Column(DECIMAL(18, 2))
    week_52_low = Column(DECIMAL(18, 2))
    analyst_rating = Column(String(50))
    target_price = Column(DECIMAL(18, 2))
    risk_level = Column(String(50))
