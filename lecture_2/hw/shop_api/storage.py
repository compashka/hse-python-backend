from typing import Dict, Any

class Generator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Generator, cls).__new__(cls)
            cls._instance.item_id_counter = 1
            cls._instance.cart_id_counter = 1
        return cls._instance

    def generate_item_id(self) -> int:
        item_id = self.item_id_counter
        self.item_id_counter += 1
        return item_id

    def generate_cart_id(self) -> int:
        cart_id = self.cart_id_counter
        self.cart_id_counter += 1
        return cart_id

generator = Generator()
items_db: Dict[int, Dict[str, Any]] = {}
carts_db: Dict[int, Dict[str, Any]] = {}
