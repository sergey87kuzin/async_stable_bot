import requests

from handlers import _create_new_order, _update_order_payment_url
from handlers.site_settings import get_site_settings
from models.orders import OrderCreate
from settings import PAYMENT_URL


def create_prodamus_order_object(order):
    order_string = f"?order_id={order.id}&products[0][price]={order.total_cost}" \
                   "&products[0][quantity]=1&products[0][name]=Обучающие материалы&do=link"
    return order_string


async def create_order_from_menu(tariff, user, session):
    site_settings = await get_site_settings(session)
    TARIFF_COSTS = {
        "day": {
            "cost": site_settings.day_tariff_cost,
            "days": 30,
            "message_count": site_settings.day_tariff_count
        },
        "month": {
            "cost": site_settings.month_tariff_cost,
            "days": 30,
            "message_count": site_settings.month_tariff_count
        }
    }
    order_data = TARIFF_COSTS.get(tariff)
    if not order_data:
        return ""
    order_data = OrderCreate(
        user_id=user.id,
        total_cost=order_data.get("cost"),
        days=order_data.get("days"),
        message_count=order_data.get("message_count")
    )
    order = await _create_new_order(order_data, session)
    order_string = create_prodamus_order_object(order)
    response = requests.get(
        url=PAYMENT_URL + order_string,
        headers={
            "Content-type": "text/plain;charset=utf-8"
        },
    )
    if not response.text:
        return ""
    if not await _update_order_payment_url(order.id, response.text, session):
        return ""
    return response.text
