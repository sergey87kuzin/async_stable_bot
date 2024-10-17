from typing import Union

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from models.orders import OrderCreate
from schemas import Order

__all__ = (
    "OrderDAL",
)


class OrderDAL:
    """Data Access Layer for Users"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_order(self, order_data: OrderCreate) -> Order:
        new_order = Order(
            user_id=order_data.user_id,
            total_cost=order_data.total_cost,
            days=order_data.days,
            message_count=order_data.message_count,
            created_at=order_data.created_at,
        )
        self.db_session.add(new_order)
        await self.db_session.flush()
        return new_order

    async def update_order(self, order_id: int, payment_url: str) -> Union[str, None]:
        query = (
            update(Order)
            .where(Order.id == order_id)
            .values(payment_url=payment_url)
            .returning(Order.id)
        )
        result = await self.db_session.execute(query)
        updated_order_id_row = result.fetchone()
        if updated_order_id_row:
            return updated_order_id_row[0]
