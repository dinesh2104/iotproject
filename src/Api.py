from mongogettersetter import MongoGetterSetter
from src.Database import Database
from uuid import uuid4
from time import time
from src import md5_hash

db = Database.get_connection()

class ApiCollection(metaclass=MongoGetterSetter):
    def __init__(self, _id):
        self._collection = db.api_keys
        self._filter_query = {'$or': [
            {'id': _id},
            {'hash': _id}
        ]}
        
class Api:
    def __init__(self, _id):
        self.collection = ApiCollection(_id)
        try:
            self.id = str(self.collection.id)
        except TypeError:
            raise Exception("API Key not found")
        
    def is_valid(self):
        login_time = self.collection.time
        validity = self.collection.validity
        if validity == 0:
            return self.collection.active # means its valid forever
        else:
            if self.collection.active:
                now = time()
                return now - login_time < validity
            else:
                return False
    
    def delete(self):
        self.collection.delete()
        
    @staticmethod
    def get_all_keys(session):
        if not session.get('authenticated') or not session.get('username'):
            raise Exception("User not authenticated")
        
        collection = db.api_keys
        username = session.get('username')
        result = collection.find({"username": username})
        return result
        
    @staticmethod
    def register_apikey(session, name, group, remarks, request=None, validity=0, _type="api"):
        if not session.get('authenticated') or not session.get('username'):
            raise Exception("User not authenticated")
        
        uuid = str(uuid4())
        collection = db.api_keys
        username = session.get('username')
        if request is not None:
            request_info = {
                'ip': request.remote_addr,
                'user_agent': request.headers.get('User-Agent'),
                'method': request.method,
                'url': request.url,
                'headers': dict(request.headers),
                'data': request.get_data().decode('utf-8')
            }
        else:
            request_info = None
        
        result = collection.insert_one({
            "id": uuid,
            "hash": md5_hash(uuid),
            "username": username,
            "name": name,
            "group": group,
            "remarks": remarks,
            "time": time(),
            "validity": validity, # 7 days,
            "active": True,
            "type": _type, 
            "request": request_info 
        })
        
        return uuid
        
