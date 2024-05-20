import datetime
import json

from app.models.check_record import Check_record
from app.models.cash_receipt import Cash_receipt
from app.models.product import Product
from app.extensions import db

from flask import request, session, make_response, jsonify, render_template

from app.check import bp
from app.models.profile import Profile


@bp.route('/check/<int:id_>/')
def check(id_):
    cash_rec = db.session.query(Cash_receipt).filter(Cash_receipt.id == id_).one()
    records = db.session.query(Check_record).filter(Check_record.check_id == id_).all()
    prof = None
    if cash_rec.user_id:
        prof = db.session.query(Profile).filter(Profile.id == cash_rec.user_id)
    info = {'id': cash_rec.id, 'datetime': cash_rec.check_datetime.strftime("%d.%m.%Y %H:%M"), 'ct': cash_rec.cash_type}
    products = []
    total = 0;
    for item in records:
        title = db.session.query(Product.title).filter(Product.id == item.product_id).one()[0]
        products.append({'title': title, 'cost': item.cost, 'amount': item.amount, "total": item.amount*item.cost})
        total += item.cost*item.amount
    info['products'] = products
    return render_template('check.html', info=info, prof=prof, total=total)


@bp.route('/take_check', methods=["POST"])
def take_check():
    req_json = json.loads(request.data)
    print(req_json)
    cash_rec = Cash_receipt(check_datetime=datetime.datetime.now(), cash_type=req_json["ct"])
    if 'login' in session and 'password' in session:
        user_id = db.session.query(Profile.id).filter((Profile.login == session["login"]) & (Profile.password == session["password"])).first() or None
        if user_id:
             cash_rec=Cash_receipt(check_datetime=datetime.datetime.now(), user_id=user_id)

    db.session.add(cash_rec)
    db.session.commit()
    max_check_num = db.session.query(Cash_receipt.id).order_by(Cash_receipt.id.desc()).first()[0] or 1
    for item in req_json['product_s']:
        amount = db.session.query(Product.amount).filter(Product.id == item['id']).first()[0]
        new_amount = amount-item['curr_amount']
        db.session.query(Product).filter(Product.id == item['id']).update({'amount':new_amount})
        db.session.commit()
        db.session.add(Check_record(check_id=max_check_num, product_id = item['id'], amount=item['curr_amount'], cost=item['cost']))
        db.session.commit()
    resp_json = {'id':max_check_num}

    return jsonify(resp_json)
