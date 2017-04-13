
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Crypto.Hash import MD5
from Crypto.Hash import HMAC
import os
import sys
sys.path.append(os.path.realpath('..'))
from util.tool import md5Obj
import time
#DBConfigure
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

class UserInfo(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True, nullable=False)
    pwd=db.Column(db.String(64), nullable=False)
    uid = db.Column(db.String(32),unique=True,nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

class User:
    @staticmethod
    def add(name,pwd,uid):
        try:
            db.session.add(UserInfo(name=name,pwd=pwd,uid=uid))
            db.session.commit()
        except:
            return False
        return True

    @staticmethod
    def checkUser(name,pwd):
        return UserInfo.query.filter_by(name=name).filter_by(pwd=pwd).first()

    @staticmethod
    def update(name,pwd):
        md5tool = MD5.new()
        md5tool.update(pwd)
        pwd = md5tool.hexdigest()
        temp = UserInfo.query.filter_by(name=name)
        temp.pwd=pwd
        db.session.add(UserInfo(temp))
        db.session.commit()

    @staticmethod
    def get_uid(name):
        return UserInfo.query.filter_by(name=name).first()