# import blueprint
from sqlalchemy import inspect, func, text

from app.models.profile import Profile
from app.price import bp
# flask modules
from flask import render_template, request, jsonify, session, make_response
# import db
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import SubCategory
from app.extensions import db

import json


@bp.route("/price", methods=['GET', 'POST'])
def price():
    profile = None
    if "login" in session: profile = db.session.query(Profile.id).filter((Profile.login == session["login"])|(Profile.password == session["password"])).first() or None
    if not request.args:
        products = Product.query.all()
        categories = Category.query.all()
        min_cost = db.session.query(func.min(Product.cost)).first()[0] or 0
        print(min_cost)
        max_cost = db.session.query(func.max(Product.cost)).first()[0] or 0
        # print(products)
        return render_template('price.html', products=products, categories=categories, mm=[min_cost, max_cost], profile = profile)
    else:
        search = request.args.get('search') or None
        if search:
            query = 'SELECT * FROM product WHERE '
            for i in search.split(' '):
                if query.find('like') == -1:
                    query += f"upper(title) like upper('%{i}%')"
                else:
                    query += f" and upper(title) like upper('%{i}%')"
            print(query)
            query = text(query)
            result = db.session.execute(query)
            categories = Category.query.all()
            return render_template('price.html', products=result, categories=categories, profile = profile)

        category = request.args.get("category") or None
        subcategory = request.args.get("subcategory") or None
        sort = request.args.get("sort") or None
        #from_ = request.form.get("from") or None
        #to_ = request.form.get("to") or None
        query = "SELECT * FROM product"

        if category:
            query += f" WHERE cat_id = {category}"

        if subcategory:
            query += f" AND subcat_id = {subcategory}"

       # if from_ and to_:
          #  if query.find("WHERE") > -1:
          #      query += f" AND 'cost' BETWEEN {from_} AND {to_}"
          #  else:
          #      query += f" WHERE 'cost' BETWEEN {from_} AND {to_}"

        if sort:
            if sort == "rich":
                query += " ORDER BY cost DESC"
            if sort == "chip":
                query += " ORDER BY cost ASC"

        print(query)

        query = text(query)
        result = db.session.execute(query)
        categories = Category.query.all()
        min_cost = 0
        max_cost = 0
        #for i in result:
         #   print(i.title)
            #if min_cost > i.cost:
           #     min_cost = i.cost
           # if max_cost < i.cost:
            #    max_cost = i.cost
        #print(min_cost)
        #print(max_cost)
        #if result: print("exist")


        return render_template('price.html', products=result, categories=categories, profile = profile)


@bp.route('/search', methods=['POST'])
def search():
    search = request.form.get('search') or None
    if not search:
        return '<script>alert("Плохой запрос"); location.href = "/price";</script>'
    query = 'SELECT * FROM product WHERE '
    for i in search.split(' '):
        if query.find('like') == -1:
            query += f"upper('title') like '%{i}%'"
        else:
            query += f" or upper('title') like '%{i}%'"
    query = text(query)
    result = db.session.execute(query)
    categories = Category.query.all()
    return render_template('price.html', products=result, categories=categories)

def object_as_dict(obj):
    return {
        c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs
    }

@bp.route('/subcats', methods=['POST'])
def subcats():
    data = json.loads(request.data)
    text = data.get("id_cat",None)
    print(text)
    subcats_ = db.session.query(SubCategory).filter(SubCategory.cat_id == text).all()
    subcats_array = []
    for i in subcats_:
        subcats_array.append(object_as_dict(i))
    return jsonify(subcats_array)


@bp.route('/products', methods=["GET", "POST"])
def products():
    data = json.loads(request.data)
    print(data)
    id_cat_ = data.get("id_cat", None) or None
    id_subcat_ = data.get("id_subcat", None) or None


    query = "SELECT * FROM product"

    if id_cat_ and id_subcat_:
        print('first')
        query = f"SELECT id, title FROM product WHERE cat_id = {id_cat_} AND subcat_id = {id_subcat_}"
    elif id_cat_ and not id_subcat_:
        print('second')
        query = f"SELECT id, title FROM product WHERE cat_id = {id_cat_}"
    else:
        print('end')
        query = "SELECT id, title FROM product"

    query = text(query)
    result = db.session.execute(query)
    print(result)

    products_array = []
    for i in result:
        print(i)
        products_array.append({"id": i[0], "title": i[1]})
    print(products_array)
    return jsonify(products_array)


@bp.route('/product', methods=['POST'])
def get_product():
    data = json.loads(request.data)
    print(data)
    id_prod = data.get("id", None) or None

    product = db.session.query(Product).filter(Product.id == id_prod).first()

    return jsonify(object_as_dict(product))


@bp.route('/product_by_art', methods=['POST'])
def get_product_by_art():
    data = json.loads(request.data)
    print(data)
    id_prod = data.get("art", None) or None

    product = db.session.query(Product).filter(Product.article == id_prod).first() or None
    if product:
        return jsonify(object_as_dict(product))
    else:
        return make_response("Не найдено", 400)
