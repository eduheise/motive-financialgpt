from sqlalchemy import Column, String, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TargetAllocation(Base):
    """
    SQLAlchemy ORM model for the 'target_allocation' table.

    Attributes:
        client (str): The client identifier (part of the primary key).
        asset_class (str): The asset class (part of the primary key).
        target_allocation_percent (decimal): The target allocation percentage for the asset class.
    """

    __tablename__ = "target_allocation"

    client = Column(String(50), primary_key=True)
    asset_class = Column(String(50), primary_key=True)
    target_allocation_percent = Column(DECIMAL(5, 2))
