from datetime import datetime

from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi_reference.data.mock_data import generate_mock_data

# SQLite database stored in the data folder.
DATABASE_URL = "sqlite:///data/sql_database.db"

Base = declarative_base()


class Product(Base):
    """Class for the products table in the SQL database."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    product_category = Column(String, nullable=False)
    product_description = Column(String)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)


def init_sql():
    """Initializes the SQLite database with mock data."""
    engine = create_engine(DATABASE_URL)
    # create the tables defined in the Base metadata
    # NOTE: only creates tables if they do not exist
    Base.metadata.create_all(engine)
    # create a session to interact with the database
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # delete all rows in the products table
    # NOTE: this step ensures that the table is cleared before adding new data
    session.query(Product).delete()
    session.commit()

    # generate mock data and insert it into the products table
    df = generate_mock_data(1000)
    product_dicts = df.to_dicts()

    for product in product_dicts:
        new_product = Product(
            product_id=product["product_id"],
            product_name=product["product_name"],
            product_category=product["product_category"],
            product_description=product["product_description"],
            valid_from=datetime.strptime(product["valid_from"], "%Y-%m-%d"),
            valid_to=datetime.strptime(product["valid_to"], "%Y-%m-%d"),
            price=product["price"],
            stock=product["stock"],
        )
        session.add(new_product)

    # commit the changes to the database
    session.commit()


if __name__ == "__main__":
    init_sql()
