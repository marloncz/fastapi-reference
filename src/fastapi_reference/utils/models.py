from datetime import date

from pydantic import BaseModel, Field


class GeneralResponse(BaseModel):
    """General response model for the API."""

    message: str


class RandomSample(BaseModel):
    """Model for requesting a random sample of products."""

    sample_size: int = Field(..., description="Number of samples to generate")


class Product(BaseModel):
    """Model for updating / receiving products in the SQL database."""

    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    product_description: str = Field(..., description="Product description")
    product_category: str = Field(..., description="Product category")
    price: float = Field(..., description="Product price in USD")
    stock: int = Field(..., description="Product stock")
    valid_from: date = Field(
        ..., description="Date in format 'YYYY-MM-DD' when the product is valid from"
    )
    valid_to: date = Field(
        ..., description="Date in format 'YYYY-MM-DD' when the product is valid to"
    )


class UpdateProducts(BaseModel):
    """Model for updating products in the SQL darabase."""

    products: list[Product] = Field(default_factory=list, description="List of products to update")
    user_name: str = Field(..., description="Name of the user who is updating the products")
    user_email: str = Field(..., description="E-Mail of the user who is updating the products")


class ReceiveProducts(BaseModel):
    """Model for receiving products."""

    products: list[Product] = Field(default_factory=list, description="List of products")


class GetProductsRequest(BaseModel):
    """Model for getting products."""

    product_ids: list[str] = Field(default_factory=list, description="List of product IDs to get")
