import logging
from datetime import date
from typing import cast

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from fastapi_reference.data.mock_data import generate_mock_data
from fastapi_reference.utils.models import (
    GeneralResponse,
    GetProductsRequest,
    Product,
    RandomSample,
    ReceiveProducts,
    UpdateProducts,
)
from fastapi_reference.utils.sql import DATABASE_URL, ProductTable

logger = logging.getLogger(__name__)

app = FastAPI()

# CORS...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=200, response_model=GeneralResponse)
async def health():
    """Health check endpoint.

    Returns:
        The status of the service.
    """
    return GeneralResponse(message="Service is up and running.")


@app.get("/receive_sample_products", status_code=200, response_model=ReceiveProducts)
async def receive_sample_products(body: RandomSample):
    """Endpoint for receiving results based on mock data.

    Returns:
        The status of the service.
    """
    logger.info("Generating mock data with %s samples...", body.sample_size)
    mock_data = generate_mock_data(body.sample_size)
    products_list = mock_data.to_dicts()
    return ReceiveProducts(products=[Product(**product) for product in products_list])


@app.get("/receive_products_by_id", status_code=200, response_model=ReceiveProducts)
async def receive_products_by_id(body: GetProductsRequest):
    """Endpoint for receiving results.

    Returns:
        The status of the service.
    """
    engine = create_engine(DATABASE_URL)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    logger.info("Getting products with IDs: %s", ", ".join(body.product_ids))
    products = (
        session.query(ProductTable).filter(ProductTable.product_id.in_(body.product_ids)).all()
    )
    products_list = [
        {
            "product_id": cast(str, product.product_id),
            "product_name": cast(str, product.product_name),
            "product_description": cast(str, product.product_description),
            "product_category": cast(str, product.product_category),
            "price": cast(float, product.price),
            "stock": cast(int, product.stock),
            "valid_from": cast(date, product.valid_from).strftime("%Y-%m-%d"),
            "valid_to": cast(date, product.valid_to).strftime("%Y-%m-%d"),
        }
        for product in products
    ]

    return ReceiveProducts(products=[Product(**product) for product in products_list])  # type: ignore


@app.post("/update_products", status_code=200, response_model=GeneralResponse)
async def update_products(body: UpdateProducts):
    """Endpoint for updating products."""
    engine = create_engine(DATABASE_URL)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    try:
        missing_products = []
        logger.info("Updating products...")
        for product in body.products:
            db_product = (
                session.query(ProductTable)
                .filter(ProductTable.product_id == product.product_id)
                .first()
            )

            if db_product:
                db_product.product_name = product.product_name
                db_product.product_description = product.product_description
                db_product.product_category = product.product_category
                # NOTE: weird mypy issue here...
                db_product.price = float(db_product.price)  # type: ignore
                db_product.price = product.price  # type: ignore
                db_product.stock = product.stock
                db_product.valid_from = product.valid_from
                db_product.valid_to = product.valid_to
                db_product.user_email = body.user_name
                db_product.user_name = body.user_email
                session.commit()
            else:
                missing_products.append(product.product_id)
        n_update = len(body.products) - len(missing_products)
    except SQLAlchemyError as e:
        logger.error("Error: %s", e)
        session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred while updating products: {str(e)}"
        ) from e
    if missing_products:
        return GeneralResponse(
            message=f"Updated {n_update} products. "
            f"Note: Products with IDs {', '.join(missing_products)} could not be found."
        )
    return GeneralResponse(message="Products updated successfully.")


@app.post("/add_products", status_code=200, response_model=GeneralResponse)
async def add_products(body: UpdateProducts):
    """Endpoint for adding new products."""
    engine = create_engine(DATABASE_URL)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    try:
        existing_products: list[str] = []
        logger.info("Updating products...")
        for product in body.products:
            db_product = (
                session.query(ProductTable)
                .filter(ProductTable.product_id == product.product_id)
                .first()
            )

            if db_product:
                existing_products.append(str(db_product.product_id))
                continue

            new_product = ProductTable(
                product_id=product.product_id,
                product_name=product.product_name,
                product_category=product.product_category,
                product_description=product.product_description,
                valid_from=product.valid_from,
                valid_to=product.valid_to,
                price=product.price,  # type: ignore
                stock=product.stock,
                user_name=body.user_name,
                user_email=body.user_email,
            )
            session.add(new_product)

        session.commit()
        n_new = len(body.products) - len(existing_products)

    except SQLAlchemyError as e:
        logger.error("Error: %s", e)
        session.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred while adding products: {str(e)}"
        ) from e
    if existing_products:
        return GeneralResponse(
            message=f"Added {n_new} new products to DB. "
            f"Note: Products with IDs {', '.join(existing_products)} already available."
        )
    return GeneralResponse(message="Products added successfully.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
