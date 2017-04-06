from flask import Flask
from flask import request
import requests

app=Flask(__name__)
def get_app():
    return app

class Cuser():
    @staticmethod
    def authRequest():
        pass

    @staticmethod
    def authResponse():
        pass

    @staticmethod
    def regRequest():
        pass

    @staticmethod
    def loginRequest():
        pass

