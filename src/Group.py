from mongogettersetter import MongoGetterSetter
from src.Database import Database
from uuid import uuid4
from src.Api import Api
from time import time

db = Database.get_connection()

class GroupCollection(metaclass=MongoGetterSetter):
    def __init__(self, id):
        self._collection = db.groups
        self._filter_query = {
            '$or': [
                {'id': id},
                {'name': id}
            ]
        }
        
class Group:
    def __init__(self, id):
        self.collection = GroupCollection(id)
        self.id = self.collection.id

    @staticmethod
    def deleteGroup(id):
        grp=Group(id)
        collection=db.api_keys
        list_api=list(collection.find({"group":grp.collection.id}))
        if(len(list_api)==0):
            grp.collection.delete()
            return "success"
        else:
            return "API Key are linked with this group please delete the API Keys"
            
        
    @staticmethod
    def register_group(name, description):
        uuid = str(uuid4())
        collection = db.groups
        result = collection.insert_one({
            "id": uuid,
            "name": name,
            "description": description,
            "active": True,
        })
        
        return Group(uuid)
    
    @staticmethod
    def get_groups():
        collection = db.groups
        return collection.find({})
