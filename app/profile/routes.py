# import blueprint
from app.profile import bp
# flask modules
from flask import render_template, session, redirect, request, Response
# db modules
from app.extensions import db
from app.models.profile import Profile
from app.models.cart import Cart
from app.models.product import Product
from app.models.order_record import Order_Record
from app.models.orders import Orders


@bp.route("/profile/<int:id_>/")
def profile(id_):

    if 'login' not in session:
        return redirect('/login')

    login = session['login']
    password = session['password']

    cart_items = []
    profile_ = db.session.query(Profile).filter((Profile.id == id_)&(Profile.login == login)&(Profile.password == password)).first()
    cart_ = db.session.query(Cart).filter((Cart.user_id == id_)).all() or None
    if cart_:
        for item in cart_:
            cart_item = db.session.query(Product).filter(Product.id == item.product_id).first()
            cart_items.append({'id':item.id, 'title':cart_item.title, 'amount':item.amount, 'cost':item.amount*cart_item.cost})
    print(cart_items)

    orders_ = db.session.query(Orders).filter(Orders.user_id == id_).all() or None


    return render_template('profile.html', profile=profile_, cart=cart_items, orders = orders_)


@bp.route('/profile/<int:id_>/del', methods=['POST'])
def delete_item(id_):
    req_json = request.json
    print(req_json)
    item_id = req_json.get('id')
    print(item_id)
    f_del = Cart.query.filter(Cart.id == item_id).one()
    db.session.delete(f_del)
    db.session.commit()
    return Response(status=204)


@bp.route('/profile/<int:id_>/order', methods=['POST'])
def make_order():
    req_json = request.json
