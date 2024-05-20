from app.extensions import db


class Vin_order(db.Model):
    __tablename__ = "vin_order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vin = db.Column(db.String(25))
    message = db.Column(db.String(250), default = 'Позвоните мне')
    user_id = db.Column(db.Integer)
