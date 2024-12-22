from app import app,db
from datetime import datetime
from sqlalchemy import (
    text, Column, ForeignKey, Integer, String,DateTime,Text, Boolean
)
from passlib.hash import bcrypt



class User(db.Model):
    __tablename__ = 'auth_user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(Integer, primary_key = True)
    name = db.Column(String)
    firstname = db.Column(String)

    email = db.Column(String, nullable = False,unique=True)
    password_hash = db.Column(String, nullable = False)

    active = db.Column(Boolean, nullable= False, default = True)


    datecreated = db.Column(DateTime, nullable = False, default = datetime.now())

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self,value):
        self.password_hash = bcrypt.hash(value)


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






def initdb(reset=False):
    if reset:
        db.drop_all()

    db.create_all()

    g_user = User(email='guest@example.com')
    g_user.password='justpassingby'

    db.session.add(g_user)
    db.session.commit()

    db.session.flush()


if __name__ == '__main__':
    with app.app_context():
        initdb(reset=True)



