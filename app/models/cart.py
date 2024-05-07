
from app.extensions import db

class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    def __repr__(self):
        return f'<Post "{self.id}">'
