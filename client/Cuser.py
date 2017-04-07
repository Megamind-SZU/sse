from flask import Flask
from flask import request
import requests
import anydbm
import json
import os
import sys
sys.path.append(os.path.realpath('..'))
from util.tool import md5Obj
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as pkcs
from Crypto.PublicKey import RSA

default_uri = "http://127.0.0.1:7070/Request"
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

sse_key=''

class Cuser():
    @staticmethod
    def authRequest():
        if Cuser.loginRequest() == True:
            pass

    @app.route('/authResponse',methods=['POST'])
    def authResponse(self):
        if request.method == 'POST':
            type = request.form['type']
            p = request.form['p']
            if type == TYPE_AUTH_GETKEY:
                pass
            elif type == TYPE_AUTH_UPDATE:
                uf = request.form['uf']
                s = raw_input(uf+" request auth from you|A(accept) or R(reject):")
                if s == 'A':
                    enc_key = get_enc_key(p)
                    result = {
                        'type':TYPE_AUTH_OK,
                        'authkey':enc_key
                    }
                elif s == 'R':
                    result = {
                        'type':TYPE_AUTH_FAIL,
                        'authkey':None
                    }

            result = json.dumps(result)
            return result

    @staticmethod
    def regRequest(name,pwd):
        pwd = md5Obj(pwd)
        data={
            'type':TYPE_REG,
            'name':name,
            'pwd':pwd
        }
        result=requests.post(default_uri,data)
        result=json.loads(result)
        user_record(name=name,pwd=pwd)
        print result['reg']

    @staticmethod
    def loginRequest():
        data=user_record()
        data['type']=TYPE_LOGIN
        result=requests.post(default_uri,data)
        result=json.loads(result)
        return result['login']


def user_record(name='',pwd=''):
    record = anydbm.open('Urecord','c')
    data={}
    if name=='' and pwd=='':
        data = {
            'name':record['name'],
            'pwd':pwd['pwd']
        }
    elif name<>'' and pwd<>'':
        record['name'] = name
        record['name'] = pwd

    record.close()
    return data

def get_enc_key(p):
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    rsakey = RSA.importKey(p)
    cipher = pkcs.new(rsakey)
    enc_key = cipher.encrypt(sse_key)
    return enc_key

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=7080,debug=True)
