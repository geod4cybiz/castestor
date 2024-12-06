import os
from dotenv import load_dotenv
load_dotenv()


DEBUG = True
SECRET_KEY='b975e54b6356cf6036b97dJAe7MEfa4695dd1e85a2fbcdbc5fe6OB'

DATABASE_URL=os.environ.get('DATABASE_URL','sqlite:///')


SQLALCHEMY_DATABASE_URI = DATABASE_URL

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_MAX_OVERFLOW = 0

SQLALCHEMY_POOL_TIMEOUT = 5
SQLALCHEMY_POOL_RECYCLE = 1
SQLALCHEMY_TRACK_MODIFICATIONS = False


DATA_DIR = os.path.join(os.path.dirname(__file__),'data')
LOG_DIR = os.path.join(DATA_DIR,'logs')
if not os.path.isdir(LOG_DIR):
	os.makedirs(LOG_DIR)

CACHE_DIR = os.path.join(DATA_DIR,'cache')
if not os.path.isdir(CACHE_DIR):
	os.makedirs(CACHE_DIR)



