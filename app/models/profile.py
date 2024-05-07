from app.extensions import db
from app.models.cart import Cart

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(255), default="н/з")
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))
    phone_num = db.Column(db.String(20))
    email = db.Column(db.String(255))
    carts = db.relationship("Cart", backref='profile', lazy=True)

    def __repr__(self):
        return f'<Post "{self.phone_num}">'
