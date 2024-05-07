from app.extensions import db


class SubCategory(db.Model):
    __tablename__ = "subcategory"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_id = db.Column(db.Integer)
    title = db.Column(db.String(150))
