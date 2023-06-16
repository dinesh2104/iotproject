import pymongo
from src.Database import Database
from src.Session import Session
from src import get_config
from time import time
from random import randint
import bcrypt

db=Database.get_connection()
users=db.users

class User:
    def __init__(self,id):        
        #TODO construct ser object
        print("Id is {}".format(id))

    @staticmethod
    def register(username,password,confirm_pass):
        if(password!=confirm_pass):
            raise Exception("Password and Confirm Password do not match")
        salt=bcrypt.gensalt()
        hashpass=bcrypt.hashpw(password.encode(),salt)
        _id=users.insert_one({
            "username":username,
            "password":hashpass,
            "register_time":time(),
            "active":False,
            "activate_token": randint(100000,999999)
        })
        return _id

    @staticmethod
    def login(username,password,request_object=None):
        result=users.find_one({
            "username":username
        })
        if result:
            if bcrypt.checkpw(password.encode(),result['password']):
                sess=Session.register_session(username,request=request_object)
                return sess.id
            else:
                raise Exception('Incorrect Password')
        else:
            raise Exception("Incorrect Credential")


