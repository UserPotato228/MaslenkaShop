from flask import Blueprint

bp = Blueprint('check', __name__)
from app.check import routes
