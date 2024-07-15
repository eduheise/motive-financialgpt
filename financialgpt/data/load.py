import numpy as np
from sqlalchemy import (
    create_engine,
    text,
)
from sqlalchemy.orm import sessionmaker
import pandas as pd
from typing import Type
from sqlalchemy.ext.declarative import DeclarativeMeta

ENGINE = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/DB")


def delete_existing_data() -> None:
    """
    Deletes all data from the specified tables in the database.

    This function connects to the database using SQLAlchemy's sessionmaker,
    executes DELETE statements for the specified tables, and commits the changes.
    """
    Session = sessionmaker(bind=ENGINE)
    session = Session()

    session.execute(text("DELETE FROM client_allocation"))
    session.execute(text("DELETE FROM target_allocation"))
    session.execute(text("DELETE FROM client_profile"))
    session.execute(text("DELETE FROM asset_performance"))

    session.commit()


def load_data(df: pd.DataFrame, SQLTable: Type[DeclarativeMeta]) -> None:
    """
    Loads data from a DataFrame into a specified SQL table.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to load.
        SQLTable (Type[DeclarativeMeta]): The SQLAlchemy table class into which the data will be loaded.

    This function replaces NaN values in the DataFrame with None, converts the DataFrame to a list of dictionaries,
    and then adds each dictionary as a row in the specified SQL table. If an error occurs, the transaction is rolled back.
    """
    Session = sessionmaker(bind=ENGINE)
    session = Session()

    df = df.replace({np.nan: None})

    rows = df.to_dict(orient="records")

    try:
        for row in rows:
            session.add(SQLTable(**row))
        session.commit()
        print(f"{SQLTable.__tablename__} data loaded successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error loading {SQLTable.__tablename__} data: {e}")
    finally:
        session.close()
