from typing import List, Optional
from pydantic import BaseModel, field_validator, ConfigDict

class Item(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False

class ItemCreate(BaseModel):
    name: str
    price: float

    @field_validator('price')
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Price should be positive')
        return v

    model_config = ConfigDict(extra='forbid')

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

    @field_validator('price')
    def price_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price should be positive')
        return v

    model_config = ConfigDict(extra='forbid')

class CartItem(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool

class Cart(BaseModel):
    id: int
    items: List[CartItem]
    price: float
