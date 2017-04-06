import anydbm
import user
from flask import Flask
import os
import sys
sys.path.append(os.path.realpath('..'))
from user.user import User
import user
from util import tool
import requests
from flask import request
import json


TYPE_AUTH=0x00
TYPE_REG=0x01
TYPE_AUTH_UPDATE=0x02
TYPE_AUTH_GETKEY=0x03
TYPE_AUTH_OK=0x05
TYPE_AUTH_FAIL=0x06
TYPE_LOGIN=0x07


app=Flask(__name__)
def get_app():
    return app


class Suser(user):
    def __init__(self):
        self.name = ''
        self.id = ''
        self.pwd = ''
    @app.route('/Request',methods=['POST'])
    def request(self):
        data={}
        if request.method == 'POST':

            type = request.form['type']
            data = request.form['data']

            if type == TYPE_AUTH:
                data = self.requestAuth(data['u1'],data['u2'],data['p'])
            elif type == TYPE_REG:
                data = self.reg(data['name'],data['id'],data['pwd'])
            elif type == TYPE_LOGIN:
                data = self.login(data['name'],data['pwd'])

        data = json.dumps(data)
        return data

    def login(self,name,pwd):
        if User.checkUser(name,pwd) is not None:
            return {'login':True}
        else:
            return {'login':False}

    def reg(self,name,id,pwd):
        if User.add(id=id,name=name,pwd=pwd) == True:
            return {'reg':'success to register'}
        return {'reg':'fail to register'}

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
            result = requests.post('',data)
            result = json.loads(result)
            data=auth_receive(uf,ut,result)
        elif auth == 1:
            data={
                'TYPE':TYPE_AUTH_GETKEY,
                'pubkey':p
            }
        elif auth == -1:
            data={
                'msg':'you have no auth to search',
                'authkey':None,
            }
        index.close()
        return data

    def response(self,url,data):
        url=''
        requests.post(url,data)


def auth_receive(uf,ut,data):
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
    return _data

if __name__ == '__main__':
    pass

