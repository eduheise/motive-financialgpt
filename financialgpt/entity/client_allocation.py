from sqlalchemy import Column, String, Date, DECIMAL
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ClientAllocation(Base):
    """
    SQLAlchemy ORM model for the 'client_allocation' table.

    Attributes:
        client (str): The client identifier (part of the primary key).
        symbol (str): The asset symbol (part of the primary key).
        quantity (decimal): The quantity of the asset allocated to the client.
        buy_price (decimal, optional): The buy price of the asset.
        purchase_date (date, optional): The date when the asset was purchased.
    """

    __tablename__ = "client_allocation"

    client = Column(String(50), primary_key=True)
    symbol = Column(String(50), primary_key=True)
    quantity = Column(DECIMAL(18, 2))
    buy_price = Column(DECIMAL(18, 2), nullable=True)
    purchase_date = Column(Date, nullable=True)
