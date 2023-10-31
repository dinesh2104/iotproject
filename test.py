from src import get_config
from src.User import User
from src.Database import Database
from flask import Blueprint,render_template,redirect,url_for,request,session
from pymongo import MongoClient
from mongogettersetter import MongoGetterSetter

# uid=User.register("Dinesh","dinesh","dinesh")
# print(uid)

# try:
#     if(User.login("Dinesh","dinesh1")):
#         print("login success")
# except Exception as e:
#     print("Login Failed")

# db=Database.get_connection()
# collection = db["sessions"]

# class SessionCollection(metaclass=MongoGetterSetter):
#     def __init__(self, _id):
#         self._filter_query ={"id": _id}# or the ObjectID, at your convinence
#         self._collection = collection # Should be a pymongo.MongoClient[database].collection

# class Session:
#     def __init__(self,id1="d5909851-be13-43b1-9bb0-f26ad657768e"):
#         self.sid=id1
#         print("id1:",id1)
#         self.collection=SessionCollection(id1)
#         print(self.collection)


# try:
#     ssid="192e20f5-d9bc-4a6f-96df-3baf9a87cba3"
#     sobj=Session(ssid)
#     print(sobj)
#     print(sobj.collection.delete())
    
#     print(sobj)
# except Exception as e:
#     print(e)

u=User("dinesh@gmail.com")
print(u.collection['active'])