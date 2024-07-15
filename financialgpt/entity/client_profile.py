from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ClientProfile(Base):
    """
    SQLAlchemy ORM model for the 'client_profile' table.

    Attributes:
        client (str): The client identifier (primary key).
        target_portfolio (str): The target portfolio assigned to the client.
    """

    __tablename__ = "client_profile"

    client = Column(String(50), primary_key=True)
    target_portfolio = Column(String(100), nullable=False)
