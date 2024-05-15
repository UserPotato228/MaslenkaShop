from flask import request, render_template, session
from sqlalchemy import func

from app.models.orders import Orders
from app.models.profile import Profile
from app.order import bp

from app.extensions import db
from app.models.cart import Cart
from app.models.product import Product
from app.models.order_record import Order_Record

import json


@bp.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        items = json.loads(request.args.get('items'))
        print(items)
        items_arr = []
        order_items = []
        total_cost = 0
        for item in items:
            items_arr.append(db.session.query(Cart).filter(Cart.id == item['id']).first())
        for item in items_arr:
            cart_item = db.session.query(Product).filter(Product.id == item.product_id).first()
            order_items.append({'id':item.id, 'title':cart_item.title, 'amount':item.amount, 'cost':item.amount*cart_item.cost})
            total_cost += item.amount*cart_item.cost
        return render_template('order.html', order_items = order_items, total_cost=total_cost)

    else:
        max_order_num = db.session.query(Orders).order_by(Orders.id.desc()).first()[0] or 1
        print(max_order_num)
        items = json.loads(request.form.get('items')) or None
        print(items)
        if items is None:
            return "something wrong :/"

        db.session.add(Orders(status="В процессе", user_id=db.session.query(Profile.id).filter((Profile.login == session["login"])|(Profile.password == session["password"])).first()[0]))
        db.session.commit()

        items_arr = []
        for item in items:
            items_arr.append(db.session.query(Cart).filter(Cart.id == item['id']).first())
            Cart.query.filter(Cart.id == item['id']).one()
        for item in items_arr:
            cart_item = db.session.query(Product).filter(Product.id == item.product_id).first()
            db.session.add(Order_Record(order_id=max_order_num, user_id = db.session.query(Profile.id).filter((Profile.login == session["login"])|(Profile.password == session["password"])).first()[0], product_id=item.product_id, amount=item.amount))
            db.session.commit()
            print(cart_item.id)
            db.session.delete(Cart.query.filter(Cart.id == item.id).one())
            db.session.commit()


        return "Ваш заказ: НОМЕР_ЗАКАЗА<br>Он будет обработан в течении рабочего дня."

