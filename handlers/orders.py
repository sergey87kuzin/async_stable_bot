from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from dals.orders_dal import OrderDAL
from models.orders import OrderCreate, ShowOrder


__all__ = (
    "_create_new_order",
    "_update_order_payment_url"
)


async def _create_new_order(body: OrderCreate, session: AsyncSession) -> ShowOrder:
    # async with session.begin():
    order_dal = OrderDAL(session)
    order = await order_dal.create_order(body)
    await session.commit()
    return ShowOrder(
        id=order.id,
        total_cost=order.total_cost,
        days=order.days,
        message_count=order.message_count,
    )


async def _update_order_payment_url(order_id: int, payment_url: str, session: AsyncSession) -> Union[str, None]:
    async with session.begin():
        order_dal = OrderDAL(session)
        return await order_dal.update_order(order_id=order_id, payment_url=payment_url)
