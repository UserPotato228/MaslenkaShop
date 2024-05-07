#####################
# flask config file #
#####################
# imports
import random, os

# base app dir
base_dir = os.path.abspath(os.path.dirname(__file__))

# config class
class Config:
	# max file length
	MAX_CONTENT_LENGTH = 8 * 1000 * 1000
	#alloed ext for upload
	ALLOWED_EXTENSIONS = {"webp", "jpg", "jpeg", "png", "gif", "wav", "mp4", "mp3"}
	# folder for upload
	UPLOAD_FOLDER = os.path.join(base_dir, "app", "static","Img")
	# session secret key
	SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(random.randint(1, 10))
	# database uri
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or "postgresql://postgres:reg1ss@192.168.1.175:5432/maslenka"
