from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import os
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

app = Flask(__name__)

app.config.from_object('settings')


file_handler =  RotatingFileHandler(
	os.path.join(app.config['LOG_DIR'],'app.log'),
	mode='a', maxBytes=10 * 1024 * 1024, backupCount=5	
	)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(Formatter(
	'%(asctime)s %(levelname)s: %(message)s '
	'[in %(pathname)s:%(lineno)d]'
))

app.logger.addHandler(file_handler)
app.jinja_env.add_extension('jinja2.ext.do')

logger = app.logger

db = SQLAlchemy(app)

from app.cas.views import urls as cas_urls,login as cas_login,logout as cas_logout
app.register_blueprint(cas_urls)


babel = Babel(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return cas_login()
