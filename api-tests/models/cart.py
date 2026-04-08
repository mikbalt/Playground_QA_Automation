from pydantic import BaseModel


class CartProduct(BaseModel):
    id: int
    title: str
    price: float
    quantity: int
    total: float
    discountPercentage: float
    discountedTotal: float | None = None
    discountedPrice: float | None = None
    thumbnail: str


class Cart(BaseModel):
    id: int
    products: list[CartProduct]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int
