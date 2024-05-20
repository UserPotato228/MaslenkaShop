from app.extensions import db


class Check_record(db.Model):
    __tablename__ = "check_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    check_id = db.Column(db.Integer, db.ForeignKey("cash_receipt.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    amount = db.Column(db.Integer, default=1)
    cost = db.Column(db.Integer, default=1)
