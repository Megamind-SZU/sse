
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Crypto.Hash import MD5
import os
import sys
sys.path.append(os.path.realpath('../util'))
import tool
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

    def __repr__(self):
        return '<User %r>' % self.name

class User:
    @staticmethod
    def add(id,name,pwd):
        pwd=tool.md5Obj(pwd)
        try:
            db.session.add(UserInfo(id=id,name=name,pwd=pwd))
            db.session.commit()
        except:
            return 'fail to add'
        return 'success to add'

    @staticmethod
    def checkUser(name,pwd):
        md5tool = MD5.new()
        md5tool.update(pwd)
        pwd = md5tool.hexdigest()
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