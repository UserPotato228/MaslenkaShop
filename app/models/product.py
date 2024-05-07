from app.extensions import db

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255), default="н/з")
    cost = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    cat_id = db.Column(db.Integer)
    subcat_id = db.column(db.Integer)
    photo_path = db.Column(db.String(150), default="Default.png")



