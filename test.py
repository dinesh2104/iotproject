from src import get_config
from src.User import User
from src.Database import Database
from pymongo import MongoClient
from mongogettersetter import MongoGetterSetter

# uid=User.register("Dinesh","dinesh","dinesh")
# print(uid)

# try:
#     if(User.login("Dinesh","dinesh1")):
#         print("login success")
# except Exception as e:
#     print("Login Failed")

db=Database.get_connection()
collection = db["employee"]
class Employee(metaclass=MongoGetterSetter):
    def __init__(self, _id):
        self._filter_query = {"id": _id} # or the ObjectID, at your convinence
        self._collection = collection # Should be a pymongo.MongoClient[database].collection

    # if the document doesn't exist, we could create it here
        try:
            self._id # if the document doesn't exist, self._id will raise Attribute Error
        except AttributeError or KeyError:
            self._collection.insert_one(self._filter_query)

