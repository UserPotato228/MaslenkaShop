from flask import request, render_template
from app.order import bp

from app.extensions import db
from app.models.cart import Cart
from app.models.product import Product

import json

@bp.route('/order')
def order():
    items = json.loads(request.args.get('items'))
    print(items)
    items_arr = []
    order_items = []
    for item in items:
        items_arr.append(db.session.query(Cart).filter(Cart.id == item['id']).first())
    for item in items_arr:
        cart_item = db.session.query(Product).filter(Product.id == item.product_id).first()
        order_items.append({'id':item.id, 'title':cart_item.title, 'amount':item.amount, 'cost':item.amount*cart_item.cost})

    return render_template('order.html', order_items = order_items)
