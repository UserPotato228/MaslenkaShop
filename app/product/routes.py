from flask import render_template, session, request, redirect

from app.models.cart import Cart
from app.product import bp
from app.extensions import db
from app.models.product import Product
from app.models.profile import Profile

def redirect_with_message(message, href):
    return f"<script>alert('{message}'); location.href = '{href}'</script>"

@bp.route('/price/<int:id>/', methods=['GET','POST'])
def product_view(id):
    profile = None
    if "login" in session: profile = db.session.query(Profile.id).filter((Profile.login == session["login"])|(Profile.password == session["password"])).first() or None
    if request.method == "GET":
        print(id)
        product = db.session.query(Product).filter(Product.id==id).first()
        return render_template("product.html", product=product, profile=profile)
    else:
        amount = request.form.get('amount', None) or None
        cart = Cart(amount = amount, user_id = profile.id, product_id=id)
        db.session.add(cart)
        db.session.commit()
        return redirect_with_message("Товар добавлен в корзину. Просмотреть ее можно в профиле.", request.url)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")

