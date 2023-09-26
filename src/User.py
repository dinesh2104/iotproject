import pymongo
from src.Database import Database
from src.Session import Session
from src import get_config
from time import time
from random import randint
import bcrypt
from mongogettersetter import MongoGetterSetter
from uuid import uuid4

db=Database.get_connection()
users=db.users

class UserCollection(metaclass=MongoGetterSetter):
    def __init__(self,username) -> None:
        self._collection = db.users
        self._filter_query = {
            "$or": [
                {"username": username}, 
                {"id": username}
            ]
        }


class User:
    def __init__(self,id):        
        self.collection=UserCollection(id)
        self.id=self.collection.id
        self.username = self.collection.username 

    @staticmethod
    def register(username,password,confirm_pass,name,email):
        uuid = str(uuid4())
        if(password!=confirm_pass):
            raise Exception("Password and Confirm Password do not match")
        salt=bcrypt.gensalt()
        hashpass=bcrypt.hashpw(password.encode(),salt)
        _id = users.insert_one({
            "username": username, # TODO: Make as unique index to avoid duplicate entries
            "password": hashpass,
            "register_time": time(),
            "active": False,
            "activate_token": randint(100000, 999999),
            "id": uuid,
            "name": name,
            "email": email
        })

        return uuid

    @staticmethod
    def login(username,password,request_object=None):
        result=users.find_one({
            "username":username
        })
        if result:
            if bcrypt.checkpw(password.encode(),result['password']):
                sess=Session.register_session(username,request=request_object)
                return sess
            else:
                raise Exception('Incorrect Password')
        else:
            raise Exception("Incorrect Credential")


