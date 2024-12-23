from flask import Flask,render_template
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import os
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_login import current_user
from flask_caching import Cache

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
cache = Cache(app,config=app.config)

from app.cas.views import urls as cas_urls,login as cas_login,logout as cas_logout
app.register_blueprint(cas_urls)


babel = Babel(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return cas_login()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return cas_logout()

@app.route('/')
def home():
    authenticated = current_user.is_authenticated if current_user else False
    return render_template('home.html',authenticated=authenticated)
