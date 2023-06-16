from mongogettersetter import MongoGetterSetter
from src import get_config
from uuid import uuid4
from time import time
from src.Database import Database

db=Database.get_connection()

class SessionCollection(metaclass=MongoGetterSetter):
    def __init__(self,id):
        self._collection=db.sessions
        self._filter_query={"id":id}


class Session:
    def __init__(self,id):
        self.id=id
        self.collection=SessionCollection(id)

    @staticmethod
    def register_session(username,request=None,validity=604800,auth_type="plain"):
        uuid=uuid4()
        collection=db.sessions

        if request is not None:
            request_info={
                'ip':request.remote_addr,
                'user_agent':request.user_agent.string
            }

        collection.insert_one({
            "id":str(uuid),
            "username":username,
            "time":time(),
            "validity":validity,
            "active":True,
            "type":auth_type,
            "request":request_info
        })
        return Session(uuid)