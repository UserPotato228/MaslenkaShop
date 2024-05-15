from app.extensions import db


class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(20), default="В процессе")
    user_id = db.Column(db.Integer)
