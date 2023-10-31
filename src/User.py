from src.Database import Database
from src.Session import Session
from src import get_config
from time import time
from random import randint
import bcrypt
import requests
from requests.structures import CaseInsensitiveDict
from mongogettersetter import MongoGetterSetter
from uuid import uuid4
from itsdangerous.url_safe import URLSafeTimedSerializer

db=Database.get_connection()
users=db.users

class UserCollection(metaclass=MongoGetterSetter):
    def __init__(self,username) -> None:
        self._collection = db.users
        self._filter_query = {
            "$or": [
                {"username": username}, 
                {"id": username},
                {"email":username}
            ]
        }


class User:
    def __init__(self,id):        
        self.collection=UserCollection(id)
        self.id=self.collection.id
        self.username = self.collection.username 

    def changeName(self,newName):
        self.collection['name']=newName

    def changePassword(self,newPasword):
        salt=bcrypt.gensalt()
        hashpass=bcrypt.hashpw(newPasword.encode(),salt)
        self.collection['password']=hashpass

    @staticmethod
    def generate_token(email):
        serializer = URLSafeTimedSerializer(get_config("secret_key"))
        return serializer.dumps(email, salt=get_config("SECURITY_PASSWORD_SALT"))

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(get_config("secret_key"))
        try:
            email = serializer.loads(token, salt=get_config("SECURITY_PASSWORD_SALT"), max_age=expiration)
            return email
        except Exception:
            return False

    @staticmethod
    def register(username,password,confirm_pass,name,email):
        uuid = str(uuid4())
        if(password!=confirm_pass):
            raise Exception("Password and Confirm Password do not match")
        salt=bcrypt.gensalt()
        hashpass=bcrypt.hashpw(password.encode(),salt)
        #Code check the email Validation
                                
        # url = f"https://api.emailvalidation.io/v1/info?email={email}"

        # headers = CaseInsensitiveDict()
        # headers["apikey"] = get_config("email_verify_key")

        # response = requests.get(url, headers=headers)
        # response=response.json()
        # if(response['state']=="undeliverable"):
        #     raise Exception("Email ID not valid")

        _id = users.insert_one({
            "username": username, # TODO: Make as unique index to avoid duplicate entries
            "password": hashpass,
            "register_time": time(),
            "active": False,
            "activate_token": User.generate_token(email),
            "image_url":"/images/users/blank.png",
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


