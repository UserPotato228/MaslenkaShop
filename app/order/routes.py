from flask import request, render_template, session
# from sqlalchemy import func

from app.models.orders import Orders
from app.models.profile import Profile
from app.order import bp

from app.extensions import db
from app.models.cart import Cart
from app.models.product import Product
from app.models.order_record import Order_Record
from app.models.vin_order import Vin_order

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
            if item.amount > cart_item.amount: order_items.append({'id': item.id, 'title': cart_item.title, 'amount': cart_item.amount, 'cost': cart_item.amount*cart_item.cost})
            else: order_items.append({'id': item.id, 'title': cart_item.title, 'amount': item.amount, 'cost': item.amount*cart_item.cost})
            total_cost += item.amount*cart_item.cost
        return render_template('order.html', order_items=order_items, total_cost=total_cost)

    else:
        user_id = db.session.query(Profile.id).filter((Profile.login == session["login"]) | (Profile.password == session["password"])).first()[0]

        items = json.loads(request.form.get('items')) or None
        print(items)
        if items is None:
            return "something wrong :/"

        db.session.add(Orders(status="В процессе", user_id=user_id))
        db.session.commit()

        max_order_num = db.session.query(Orders.id).filter(Orders.user_id == user_id).order_by(Orders.id.desc()).first()[0] or 1

        items_arr = []
        for item in items:
            items_arr.append(db.session.query(Cart).filter(Cart.id == item['id']).first())
            Cart.query.filter(Cart.id == item['id']).one()
        for item in items_arr:
            cart_item = db.session.query(Product).filter(Product.id == item.product_id).first()
            if cart_item.amount < item.amount: db.session.add(Order_Record(order_id=max_order_num, product_id=item.product_id, amount=cart_item.amount))
            else: db.session.add(Order_Record(order_id=max_order_num, product_id=item.product_id, amount=item.amount))
            db.session.commit()
            print(cart_item.id)
            db.session.delete(Cart.query.filter(Cart.id == item.id).one())
            db.session.commit()

        return f"<script>alert('Заказ создан. Номер вашего заказа №{max_order_num}. Он может пригодиться при получении.'); location.href='/profile/{user_id}/';</script>"


@bp.route('/vin', methods=["GET","POST"])
def vin_order():
    if request.method == "GET":
        user_id = db.session.query(Profile.id).filter((Profile.login == session["login"]) | (Profile.password == session["password"])).first()[0] or None
        if user_id:
            return render_template('vin.html')
        else:
            return "<script>alert('Чтобы отправить запрос нужно авторизоваться'); location.href='/login';</script>"
    else:
        vin = request.form.get('vin') or None
        message = request.form.get('message') or None
        user_id = db.session.query(Profile.id).filter((Profile.login == session["login"]) | (Profile.password == session["password"])).first()[0]

        if not vin or not message or not user_id:
            return "<script>alert('Одно или несколько полей не заполнены'); location.href='/vin';</script>"

        db.session.add(Vin_order(vin = vin, message = message, user_id=user_id))
        db.session.commit()

        return "<script>alert('Ваш запрос отправлен. В скором времени с вами свяжутся.'); location.href='/vin';</script>"
