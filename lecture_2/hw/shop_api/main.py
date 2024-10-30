from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from fastapi.responses import JSONResponse

from lecture_2.hw.shop_api.models import ItemCreate, ItemUpdate
from lecture_2.hw.shop_api.storage import generator, items_db, carts_db
from lecture_2.hw.shop_api.utils import calculate_cart_price

app = FastAPI(title="Shop API")

@app.post("/cart", status_code=201)
def create_cart():
    cart_id = generator.generate_cart_id()
    carts_db[cart_id] = {'id': cart_id, 'items': [], 'price': 0}
    headers = {"Location": f"/cart/{cart_id}"}
    return JSONResponse(status_code=201, content={'id': cart_id}, headers=headers)


@app.get("/cart/{cart_id}")
def get_cart(cart_id: int):
    cart = carts_db.get(cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_items = cart['items']
    cart_price = calculate_cart_price(cart_items)
    cart['price'] = cart_price
    return cart

@app.get("/cart")
def list_carts(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        min_price: Optional[float] = Query(None, ge=0),
        max_price: Optional[float] = Query(None, ge=0),
        min_quantity: Optional[int] = Query(None, ge=0),
        max_quantity: Optional[int] = Query(None, ge=0),
):
    carts = []
    for cart in carts_db.values():
        cart_items = cart['items']
        total_quantity = sum(item['quantity'] for item in cart_items)
        cart_price = calculate_cart_price(cart_items)
        if min_price is not None and cart_price < min_price:
            continue
        if max_price is not None and cart_price > max_price:
            continue
        if min_quantity is not None and total_quantity < min_quantity:
            continue
        if max_quantity is not None and total_quantity > max_quantity:
            continue
        cart_copy = cart.copy()
        cart_copy['price'] = cart_price
        carts.append(cart_copy)
    return carts[offset: offset + limit]

@app.post("/cart/{cart_id}/add/{item_id}")
def add_item_to_cart(cart_id: int, item_id: int):
    cart = carts_db.get(cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    item = items_db.get(item_id)
    if item is None or item['deleted']:
        raise HTTPException(status_code=404, detail="Item not found")

    for cart_item in cart['items']:
        if cart_item['id'] == item_id:
            cart_item['quantity'] += 1
            break
    else:
        cart_item = {
            'id': item_id,
            'name': item['name'],
            'quantity': 1,
            'available': not item['deleted'],
        }
        cart['items'].append(cart_item)
    return {"detail": "Item added to cart"}

@app.post("/item", status_code=201)
def create_item(item: ItemCreate):
    item_id = generator.generate_item_id()
    items_db[item_id] = {
        'id': item_id,
        'name': item.name,
        'price': item.price,
        'deleted': False,
    }
    headers = {"Location": f"/item/{item_id}"}
    return JSONResponse(status_code=201, content=items_db[item_id], headers=headers)

@app.get("/item/{item_id}")
def get_item(item_id: int):
    item = items_db.get(item_id)
    if item is None or item['deleted']:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/item")
def list_items(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, gt=0),
        min_price: Optional[float] = Query(None, ge=0),
        max_price: Optional[float] = Query(None, ge=0),
        show_deleted: bool = False,
):
    items = []
    for item in items_db.values():
        if not show_deleted and item['deleted']:
            continue
        if min_price is not None and item['price'] < min_price:
            continue
        if max_price is not None and item['price'] > max_price:
            continue
        items.append(item)
    return items[offset: offset + limit]

@app.put("/item/{item_id}")
def replace_item(item_id: int, item: ItemCreate):
    existing_item = items_db.get(item_id)
    if existing_item is None or existing_item['deleted']:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id].update({'name': item.name, 'price': item.price})
    return items_db[item_id]

@app.patch("/item/{item_id}")
def update_item(item_id: int, item: ItemUpdate):
    existing_item = items_db.get(item_id)
    if existing_item is None or existing_item['deleted']:
        return JSONResponse(status_code=304, content={'detail': 'Not Modified'})
    update_data = item.model_dump(exclude_unset=True)
    items_db[item_id].update(update_data)
    return items_db[item_id]

@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    existing_item = items_db.get(item_id)
    if existing_item is None:
        return HTTPException(status_code=404, detail="Item not found")
    items_db[item_id]['deleted'] = True
    return {"detail": "Item deleted"}
