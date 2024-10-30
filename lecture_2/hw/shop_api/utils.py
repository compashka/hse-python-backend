from typing import List, Dict, Any

from lecture_2.hw.shop_api.storage import items_db

def calculate_cart_price(cart_items: List[Dict[str, Any]]) -> float:
    total_price = 0.0
    for cart_item in cart_items:
        if cart_item['available']:
            item = items_db[cart_item['id']]
            total_price += item['price'] * cart_item['quantity']
    return total_price
