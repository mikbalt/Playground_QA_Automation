from typing import Any

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    tags: list[str]
    brand: str | None = None
    sku: str
    weight: float
    dimensions: dict[str, float]
    warrantyInformation: str
    shippingInformation: str
    availabilityStatus: str
    reviews: list[Any]
    returnPolicy: str
    minimumOrderQuantity: int
    meta: dict[str, Any]
    images: list[str]
    thumbnail: str


class ProductsResponse(BaseModel):
    products: list[Product]
    total: int
    skip: int
    limit: int
