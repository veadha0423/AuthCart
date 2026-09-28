from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int


class CartAdd(BaseModel):
    product_id: int
    quantity: int = 1