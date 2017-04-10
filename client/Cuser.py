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

server_uri = "http://127.0.0.1:7070/Request"
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



class Cuser():

    def __init__(self):
        self.sse_key = ''


    @staticmethod
    def authRequest(ut,uf,p):
        if Cuser.loginRequest() == True:
            data={
                'type':TYPE_AUTH,
                'ut':ut,
                'uf':uf,
                'pubkey':p
            }
            enc_key=requests.post(url=server_uri,data=data)
            enc_key = json.loads(enc_key)
            return enc_key


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
                    enc_key = self.get_enc_key(p)
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
        result=requests.post(server_uri,data)
        result=json.loads(result)
        user_record(name=name,pwd=pwd)
        print result['reg']

    @staticmethod
    def loginRequest():
        data=user_record()
        data['type']=TYPE_LOGIN
        result=requests.post(server_uri,data)
        result=json.loads(result)
        return result['login']

    def get_enc_key(self,p):
        random_generator = Random.new().read
        rsa = RSA.generate(2048, random_generator)
        rsakey = RSA.importKey(p)
        cipher = pkcs.new(rsakey)
        dec_key = cipher.encrypt(self.sse_key)
        return dec_key

    @staticmethod
    def get_dec_key(self,enc_key,prikey):
        random_generator = Random.new().read
        rsakey = RSA.importKey(prikey)
        cipher = pkcs.new(rsakey)
        dec_key = cipher.decrypt(enc_key,random_generator)
        return dec_key

    @staticmethod
    def init_authKey():
        random_generator = Random.new().read
        rsa = RSA.generate(2048,random_generator)
        private_pem = rsa.exportKey()
        public_pem = rsa.publickey().exportKey()
        return (public_pem,private_pem)

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



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=7080,debug=True)
