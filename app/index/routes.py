# import blueprint
from app.index import bp
# flask modules
from flask import render_template, session
# db stuff
from app.extensions import db
from app.models.profile import Profile

@bp.route('/')
def index():
    profile = None
    if "login" in session:
        profile = db.session.query(Profile.id).filter((Profile.login == session["login"])|(Profile.password == session["password"])).first() or None
    return render_template("index.html", profile=profile)
