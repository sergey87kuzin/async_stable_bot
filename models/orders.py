from pydantic import BaseModel

from .common import TunedModel

__all__ = (
    "OrderCreate",
)


class OrderCreate(BaseModel):
    user_id: int
    total_cost: int
    days: int
    message_count: int


class ShowOrder(TunedModel):
    id: int
    total_cost: int
    days: int
    message_count: int
