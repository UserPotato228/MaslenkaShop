# import blueprint
import json

from app.profile import bp
# flask modules
from flask import render_template, session, redirect, request, Response, make_response
# db modules
from app.extensions import db
from app.models.profile import Profile
from app.models.cart import Cart
from app.models.product import Product
from app.models.order_record import Order_Record
from app.models.orders import Orders


@bp.route("/profile/<int:id_>/", methods=['POST', 'GET'])
def profile(id_):

    if request.method == "POST":
        fullname = request.form.get('fullname') or "Н/З"
        login = request.form.get('login') or None
        phone_num = request.form.get('phone') or None
        email = request.form.get('email') or "Н/З"
        old_pass = request.form.get('old_password') or None
        new_pass = request.form.get('new_password') or None
        
        
        if not login or not phone_num:
            return f"<script>alert('Одно из важных полей не заполнены.'); location.href='{request.url}'</script>"
        
        user = db.session.query(Profile).filter((Profile.id == id_)&(Profile.password==old_pass)).first() or None
        print(user)
        if not user:
            return f"<script>alert('Неверный пароль.'); location.href='{request.url}'</script>"
        
        
        if user.login != login:
            user = db.session.query(Profile).filter(Profile.login == login).first() or None
            if user:
                return f"<script>alert('Логин занят.'); location.href='{request.url}'</script>"
            
        #user = db.session.query(Profile).filter(Profile.login == login).all()
        #if len(profiles) == 1:
        
        db.session.query(Profile).filter(Profile.id == id_).update({'fullname':fullname, 'login':login, 'phone_num':phone_num, 'email':email})
        db.session.commit()
        
        if new_pass:
            db.session.query(Profile).filter(Profile.id==id_).update({'password':new_pass})
            
        return f"<script>alert('Данные успешно обновлены.'); location.href='{request.url}'</script>"
            
        
    else:
        if 'login' not in session:
            return redirect('/login')

        login = session['login']
        password = session['password']

        cart_items = []
        profile_ = db.session.query(Profile).filter((Profile.id == id_) & (Profile.login == login) & (Profile.password == password)).first()

        if profile_.id != id_:
            return "<script>alert('Вас здесь не должно быть...'); location.href='/logout'</script>"

        cart_ = db.session.query(Cart).filter((Cart.user_id == id_)).all() or None
        if cart_:
            for item in cart_:
                cart_item = db.session.query(Product).filter(Product.id == item.product_id).first()
                cart_items.append({'id': item.id, 'title': cart_item.title, 'amount': item.amount, 'cost': item.amount*cart_item.cost, 'total_amount': cart_item.amount})
        print(cart_items)

        orders_ = db.session.query(Orders).filter(Orders.user_id == id_).all() or None
        orders_array = []

        if orders_:
            for order in orders_:
                total = 0
                order_records = db.session.query(Order_Record).filter(Order_Record.order_id == order.id).all()
                products = []
                for record in order_records:
                    product = db.session.query(Product).filter(Product.id == record.product_id).first()
                    products.append({'title': product.title, 'cost': product.cost*record.amount, 'amount': record.amount})
                    total += product.cost*record.amount
                orders_array.append({'id': order.id, 'total': total, 'status': order.status, 'records': products})

        return render_template('profile.html', profile=profile_, cart=cart_items, orders=orders_array)


@bp.route('/profile/del_cart', methods=['POST'])
def delete_item():
    user_id = db.session.query(Profile.id).filter((Profile.login == session["login"]) & (Profile.password == session["password"])).first()[0]
    if not user_id:
        return make_response("Запрос отклонён", 403)
    req_json = json.loads(request.data)
    print(req_json)
    for item in req_json:
        f_del = Cart.query.filter((Cart.id == item['id']) | (Cart.user_id == user_id)).one()
        db.session.delete(f_del)
        db.session.commit()
    return Response(status=200)


@bp.route('/profile/edit')
def edit():
    pass

@bp.route('/profile/del_order', methods=["POST"])
def delete_order():
    user_id = db.session.query(Profile.id).filter((Profile.login == session["login"]) & (Profile.password == session["password"])).first()[0]
    if not user_id:
        return make_response("Запрос отклонён", 403)

    order_id = request.json.get('id')

    for item in db.session.query(Order_Record).filter(Order_Record.order_id == order_id).all():
        amount = db.session.query(Product.amount).filter(Product.id == item.product_id).first()[0]
        db.session.query(Product).filter(Product.id == item.product_id).update({'amount':amount+item.amount})
    
    db.session.delete(Orders.query.filter((Orders.user_id == user_id) & (Orders.id == order_id)).one())
    db.session.commit()

    db.session.query(Order_Record).filter(Order_Record.order_id == order_id).delete()
    db.session.commit()

    return Response(status=200)

# @bp.route('/profile/<int:id_>/order', methods=['POST'])
# def make_order():
#    req_json = request.json
