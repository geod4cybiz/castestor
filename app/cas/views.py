# -*- coding: utf-8 -*-
from flask import (Flask, flash,Blueprint, abort,jsonify,
    Response, request, redirect, url_for,render_template,g,make_response)

from datetime import datetime
from time import time

from functools import wraps
import jwt

# import os
# from os import path
from app import app

from app.cas.forms import LoginForm
from app.cas.security import gen_ticket,decode_ticket

from app.cas.models import User

from flask_login import (LoginManager, login_user, logout_user)

from passlib.hash import bcrypt

logger = app.logger
CAS_ALLOWED_SERVICES = [
	'/',
	'http://localhost:'
]


urls = Blueprint('cas', __name__, url_prefix='/cas')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/cas/login'

@login_manager.user_loader
def load_user(userid):
    user = User.query.filter_by(id=userid).first()
    return user

# def gen_ticket(user,service,timeout=60):
#     exp = int(time()) + timeout

#     data = { 'userid':user.id , 'service': service ,'exp': exp}
#     ticket = jwt.encode(data,app.secret_key,algorithm='HS256')
#     return ticket

# def decode_ticket(ticket):
#     data = jwt.decode(ticket,app.secret_key, algorithms=['HS256'])
#     return data

def xmlresponse(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        response  = make_response(f(*args,**kwargs))
        response.headers['Content-Type']= 'text/xml'
        return response

    return decorated_function


@urls.route('/login', methods=['GET', 'POST'])
def login():
    app.logger.info(request.host)

    qs = request.args
    service = qs.get('service','/')
    if service not in CAS_ALLOWED_SERVICES:
        abort(403)

    form = LoginForm(request.form)
    error = None
    if request.method == 'POST':
        if form.validate():
            user = User.query.filter_by(email=form.username.data, active=True).first()            
            if user is not None and bcrypt.verify(form.password.data,user.password):
                login_user(user)
                t = gen_ticket(user,service)
                return redirect('%s?ticket=%s' % (service,t))
            else:
                app.logger.warning('user not found failed')
                error = 'Wrong email and/or password'
        else:
            app.logger.warning('form validation failed')
            error = 'Wrong email and/or password'

    app.logger.info(error)
    return render_template('login.html', form=form, error=error)

@urls.route('/serviceValidate')
@xmlresponse
def service_validate():
    qs = request.args
    ticket = qs.get('ticket',None)
    service = qs.get('service',None)
    if ticket is None or service is None:
        return render_template('cas/error.xml', 
            error= {
                'code': 'INVALID_REQUEST',
                'message': 'Invalid Request'
            })

    data = decode_ticket(ticket)
    exp = int(data.get('exp',0))
    if exp < time() or service != data.get('service'):
        return render_template('cas/error.xml', 
            error= {
                'code': 'INVALID_TICKET',
                'message': 'Invalid Ticket'
            })

    userid = int(data.get('userid',0))
    user = load_user(userid)
    if user is not None: 
        # TODO other user attributes (lastname, firstname, etc...)   
        return render_template('cas/success.xml', 
            username = user.email)

    return render_template('cas/error.xml', 
        error= {
            'code': 'INTERNAL_ERROR',
            'message': 'Internal Error'
        })

@urls.route('/logout')
def logout():
    logout_user()
    return redirect('/')
