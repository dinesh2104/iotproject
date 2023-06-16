from pymongo import MongoClient
from mongogettersetter import MongoGetterSetter
from src.Database import Database

# Connect to the MongoDB database and collection

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

e=Employee(4051)
print(e)
print(e._id)


