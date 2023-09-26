from mongogettersetter import MongoGetterSetter
from src import get_config
from uuid import uuid4
from time import time
from src.Database import Database

db=Database.get_connection()

class SessionCollection(metaclass=MongoGetterSetter):
    def __init__(self,id1):
        self._collection=db.sessions
        self._filter_query={"id":id1}


class Session:
    def __init__(self,id1):
        self.sid=id1
        self.collection=SessionCollection(id1)
        

    def isValid(self):
        print(self.collection)
        login_time=self.collection.time
        validity=self.collection.validity
        return time()-login_time<validity

    @staticmethod
    def register_session(username,request=None,validity=604800,auth_type="plain"):
        uuid=str(uuid4())
        collection=db.sessions

        if request is not None:
            request_info={
                'ip':request.remote_addr,
                'user_agent':request.user_agent.string
            }

        collection.insert_one({
            "id":uuid,
            "username":username,
            "time":time(),
            "validity":validity,
            "active":True,
            "type":auth_type,
            "request":request_info
        })
        return uuid