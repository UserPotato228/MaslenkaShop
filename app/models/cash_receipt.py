from sqlalchemy import func
from app.extensions import db


class Cash_receipt(db.Model):
    __tablename__ = "cash_receipt"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    check_datetime = db.Column(db.DateTime(timezone=False))
    user_id = db.Column(db.Integer)
    cash_type = db.Column(db.String(20), default="Наличные")
