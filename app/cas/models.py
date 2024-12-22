from app import db
from datetime import datetime
from sqlalchemy import (
    text, Column, ForeignKey, Integer, String,DateTime,Text, Boolean
)
from passlib.hash import bcrypt

class Group(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'cas_group'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key = True)
    name = db.Column(String, nullable = False)
    descr = db.Column(String)

    datecreated = db.Column(DateTime, nullable = False, default = datetime.now())


user_group = db.Table('cas_user_group',
    db.Column('groupid', db.Integer, db.ForeignKey('cas_group.id')),
    db.Column('userid', db.Integer, db.ForeignKey('cas_user.id')),
    info={'bind_key':'users'},
    extend_existing= True
)

class User(db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'cas_user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key = True)
    name = db.Column(String, nullable = False)
    firstname = db.Column(String, nullable = False)

    username = db.Column(String, nullable = False)
    password_hash = db.Column(String, nullable = False)
    email = db.Column(String, nullable = False)

    securitylevel = db.Column(String, nullable = False)
    active = db.Column(Boolean, nullable= False)

    groups = db.relationship('Group', secondary=user_group, backref=db.backref('users', lazy='dynamic')) 


    @property
    def password(self):
        return self.password_hash

    @password.setter
    def passsword(self,value):
        self.password_hash = bcrypt(value)


    @property
    def security_groups(self):
        retval = [ self.securitylevel ] + [ r.name for r in self.groups ]
        return retval

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False



