from app.extensions import db


class Order_Record(db.Model):
    __tablename__ = "order_record"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, default=1)
