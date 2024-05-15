from datetime import datetime
import os.path, json

from flask import render_template, session, redirect, request, make_response

import config
from app.admin import bp
from app.extensions import db
from app.models.category import Category
from app.models.product import Product
from app.models.orders import Orders
from app.models.order_record import Order_Record

def check_host(rm_host):
    file = open(os.path.join(config.base_dir,"counts.json"), "r")
    cap = file.read()
    if cap.find(rm_host)<0:
        return True
    else:
        cap_json = json.loads(cap)
        for i in cap_json:
            if i['rm_host'] == rm_host:
                if i['count'] == 3:
                    return True
                else:
                    return False


@bp.route('/admin')
def admin_panel():
    if not check_host(request.remote_addr):
        return redirect('/')

    if 'login' not in session or (session["login"] != config.Config.adm_log and session["password"] != config.Config.adm_pass):
        return redirect('/admin_auth')
    return render_template('admin.html')


@bp.route('/admin/orders')
def orders():
    orders = db.session.query(Orders).all()
    orders_array = []
    total = 0
    for order in orders:
        total = 0
        order_records = db.session.query(Order_Record).filter(Order_Record.order_id == order.id).all()
        products = []
        for record in order_records:
            product = db.session.query(Product).filter(Product.id == record.product_id).first()
            products.append({'title':product.title, 'cost':product.cost*record.amount, 'amount':record.amount})
            total += product.cost*record.amount
        orders_array.append({'id': order.id, 'total': total, 'status':order.status, 'records':products})

    return render_template("orders.html", orders = orders_array)

@bp.route('/admin/cassa')
def cassa():
    return render_template("cassa.html")

@bp.route('/admin/orders/set_done', methods=["POST"])
def set_done():
    id_order = request.form.get('id')
    db.session.query(Orders).filter(Orders.id == id_order).update({"status":"Готов"})
    db.session.commit()
    return make_response('OK', 200)


@bp.route('/admin/orders/delete', methods=["POST"])
def delete_order():
    id_order = request.form.get('id')
    records = db.session.query(Order_Record).filter(Order_Record.order_id == id_order)
    for order in records:
        curr_amount = db.session.query(Product.amount).filter(Product.id == order.product_id).first()[0]
        db.session.query(Product).filter(Product.id == order.product_id).update({"amount":curr_amount-order.amount})
        db.session.commit()
        record = Order_Record.query.filter(Order_Record.id == order.id).one()
        db.session.delete(record)
        db.session.commit()
    order = Orders.query.filter(Orders.id==id_order).one()
    db.session.delete(order)
    db.session.commit()
    return make_response("OK", 200)


@bp.route('/admin_auth', methods=["GET", "POST"])
def admin_auth():
    if request.method == "GET":
        if not check_host(request.remote_addr):
            return redirect('/')
        return render_template("admin_auth.html")
    else:
        login = request.form.get("login") or None
        password = request.form.get("password") or None

        if not login or not password:
            return '<script>alert("Все поля должны быть заполнены"); location.href="/admin_auth";</script>'

        if login == config.Config.adm_log and password == config.Config.adm_pass:
            session["login"] = config.Config.adm_log
            session["password"] = config.Config.adm_pass
            return redirect('/admin')
        else:
            file = open(os.path.join(config.base_dir,"counts.json"), "r+")
            cap = file.read()
            file.close()
            file = open(os.path.join(config.base_dir,"counts.json"), "w")
            if cap == "" or cap is None:
                file.write('[{"rm_host":"'+request.remote_addr+'", "count":1}]')
                file.close()
                return redirect('/admin_auth')
            else:
                if cap.find(request.remote_addr)<0:
                    cap_json = json.loads(cap)
                    cap_json.append(('[{"rm_host":"'+request.remote_addr+'", "count":1}]'))
                    file.write(json.dumps(cap_json))
                    file.close()
                else:
                    cap_json = json.loads(cap)
                    for i in cap_json:
                        if i['rm_host'] == request.remote_addr:
                            i['count'] += 1
                    file.write(json.dumps(cap_json))
                    file.close()
                return redirect('/admin_auth')


@bp.route('/edit', methods=["GET", "POST"])
def admin_edit():
    if request.method == "GET":

        # if not authorized as admin
        if session['login'] != config.Config.adm_log or session['password'] != config.Config.adm_pass:
            return redirect('/admin_auth')

        categories = Category.query.all()

        return render_template("prod_edit.html", categories=categories)


def check_ext(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.Config.ALLOWED_EXTENSIONS


@bp.route('/admin/add', methods=["POST"])
def add_prod():
    article = request.form.get("article") or None
    print(article)
    title = request.form.get("title") or None
    print(title)
    desc = request.form.get("desc") or None
    print(desc)
    cost = request.form.get("cost") or None
    print(cost)
    amount = request.form.get("amount") or None
    print(amount)
    cat = request.form.get("cat") or None
    print(cat)
    subcat = request.form.get("subcat") or None
    print(subcat)
    img_name = "Default.png"

    if not article or not title or not cost or not amount or not cat or not subcat:
        return make_response("NAFF", 200)

    if "file_to_upload" not in request.files:
        img_name = "Default.png"
    else:
        if request.files['file_to_upload'].filename != "":
            file = request.files['file_to_upload']
            img_name = f"{datetime.now().strftime('%d%m%Y%H%M%S')}.{img_name.split('.')[len(img_name.split('.'))-1]}"
            if file and check_ext(file.filename):
                file.save(os.path.join(config.Config.UPLOAD_FOLDER, img_name))
        else:
            img_name = "Default.png"

    product = Product(title=title, description=desc, cost =cost, amount=amount, cat_id = cat, subcat_id = subcat, photo_path=img_name, article=article)
    db.session.add(product)
    db.session.commit()

    return make_response("OK",200)


@bp.route("/admin/update", methods=["POST"])
def update_product():
    id = request.form.get("id") or None
    print(id)
    article = request.form.get("article") or None
    print(article)
    title = request.form.get("title") or None
    print(title)
    desc = request.form.get("desc") or None
    print(desc)
    cost = request.form.get("cost") or None
    print(cost)
    amount = request.form.get("amount") or None
    print(amount)
    cat = request.form.get("cat") or None
    print(cat)
    subcat = request.form.get("subcat") or None
    print(subcat)

    if not article or not id or not title or not cost or not amount or not cat or not subcat:
        return make_response("NAFF", 200)

    img_name = ""
    if "file_to_upload" in request.files:
        if request.files['file_to_upload'].filename != "":
            file = request.files['file_to_upload']
            img_name = file.filename
            img_name = f"{datetime.now().strftime('%d%m%Y%H%M%S')}.{img_name.split('.')[len(img_name.split('.'))-1]}"
            if file and check_ext(file.filename):
                file.save(os.path.join(config.Config.UPLOAD_FOLDER, img_name))

    if img_name:
        db.session.query(Product).filter(Product.id == id).update({"title":title, "description":desc, "cost":cost, "amount":amount, "cat_id":cat, "subcat_id":subcat, "photo_path":img_name, "article":article})
    else:
        db.session.query(Product).filter(Product.id == id).update({"title":title, "description":desc, "cost":cost, "amount":amount, "cat_id":cat, "subcat_id":subcat, "article":article})

    db.session.commit()
    return make_response("OK", 200)
