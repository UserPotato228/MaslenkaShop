#######################
# flask app init file #
#######################
# start \/

# import flask
from flask import Flask, send_from_directory, request

# import config for flask
from config import Config
# import other modules
import os
# db
from app.extensions import db


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	# db init
	db.init_app(app)

	# session
	app.secret_key = '0X0X0X0X1N2T8E'

	# blueprints
	from app.index import bp as index_bp
	app.register_blueprint(index_bp)
	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp)
	from app.price import bp as price_bp
	app.register_blueprint(price_bp)
	from app.product import bp as product_bp
	app.register_blueprint(product_bp)
	from app.profile import bp as profile_bp
	app.register_blueprint(profile_bp)
	from app.order import bp as order_bp
	app.register_blueprint(order_bp)
	from app.admin import bp as admin_bp
	app.register_blueprint(admin_bp)

	# on 404 error handler
	@app.errorhandler(404)
	def request_file_not_found(e):
		return f"<h1>{request.url} не найден</h1>"
	
	@app.route('/favicon.ico/')
	def favicon():
		return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

	print(app.url_map)

	return app
