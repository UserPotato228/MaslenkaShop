#####################
# flask config file #
#####################
# imports
import random, os

# base app dir
base_dir = os.path.abspath(os.path.dirname(__file__))

# config class
class Config:
	adm_log, adm_pass = "2911masl60enka", "res296hshp"
	# max file length
	MAX_CONTENT_LENGTH = 8 * 1000 * 1000
	#alloed ext for upload
	ALLOWED_EXTENSIONS = {"webp", "jpg", "jpeg", "png"}
	# folder for upload
	UPLOAD_FOLDER = os.path.join(base_dir, "app", "static")
	# session secret key
	SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(random.randint(1, 10))
	# database uri
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or "postgresql://postgres:reg1ss@188.120.224.42:5432/maslenka"
