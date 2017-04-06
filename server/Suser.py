import anydbm
import user
from flask import Flask
import os
import sys
sys.path.append(os.path.realpath('../user'))
from user import User
import user
sys.path.append(os.path.realpath('../util'))
import tool
import anydbm
import requests

TYPE_AUTH=0x00
TYPE_REG=0x01
TYPE_AUTH_UPDATE=0x02
TYPE_AUTH_GETKEY=0x03
TYPE_AUTH_RECEIVE=0x04
TYPE_AUTH_OK=0x05
TYPE_AUTH_FAIL=0x06

app=Flask(__name__)

class Suser(user):
    def __init__(self):
        self.name = ''
        self.id = ''
        self.pwd = ''
    @app.route('/serverRequest',methods=['POST'])
    def request(self,type,data):
        if type == TYPE_AUTH:
            self.requestAuth(data['u1'],data['u2'],data['p'])
        elif type == TYPE_REG:
            self.reg(data['name'],data['id'],data['pwd'])
        elif type == TYPE_AUTH_RECEIVE:
            self.auth_receive(data)
    @app.route('/login',methods=['POST'])
    def login(self,name,pwd):
        if User.checkUser(name,pwd) is not None:
            return True
        else:
            return False

    def reg(self,name,id,pwd):
        return User.add(id=id,name=name,pwd=pwd)

    def requestAuth(self,uf,ut,p):
        link=ut+'-'+uf
        link=tool.md5Obj(link)
        index=anydbm.open('userAuth','r')
        auth=0
        for k,v in index.iteritems:
            if k==link:
                auth=v
        if auth == 0:
            data={
                'TYPE':TYPE_AUTH_UPDATE,
                'user':uf
            }
            requests.post('',data)
        elif auth == 1:
            data={
                'TYPE':TYPE_AUTH_GETKEY
            }
        elif auth == -1:
            data={
                'msg':'you have no auth to search',
                'authkey':None,
            }
            self.response(data)
        index.close()
    def response(self,url,data):
        url=''
        requests.post(url,data)

    def auth_receive(self,uf,ut,data):
        if data['type']==TYPE_AUTH_OK:
            index=anydbm.open('userAuth','w+')
            link = tool.md5Obj(ut+'-'+uf)
            index[link]=1
            index.close()
            _data={
                'msg':'success to get authkey',
                'authkey':data['authkey']
            }
        elif data['type']==TYPE_AUTH_FAIL:
            index = anydbm.open('userAuth', 'w+')
            link = tool.md5Obj(ut + '-' + uf)
            index[link] = -1
            index.close()
            _data = {
                'msg': 'fail to get authkey',
                'authkey': None
            }
        self.response('',_data)


