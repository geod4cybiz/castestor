# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (BooleanField, IntegerField, StringField, TextAreaField, FileField, 
	SelectField, SelectMultipleField,PasswordField, validators)

class LoginForm(Form):
	username = StringField('Username', [ validators.DataRequired() ])
	password = PasswordField('Password', [ validators.DataRequired() ])


