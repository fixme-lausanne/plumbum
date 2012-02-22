from collections import namedtuple
from threading import Lock as TLock
import database.utils as utils
import time
import pymongo
import db

_db = None
TLOCK = TLock()
TextAndTimestamp = namedtuple('TextAndTimestamp', 'text timestamp')

class MongoDB(db.DataBase):
    DBConn = pymongo.Connection('localhost', 27017)
    DB = DBConn['plumbum']
    
    def delete(uid):
        MongoDB.DB.remove(uid)
        
    def read(uid):
        try:
            MongoDB.DB.get(uid)
        except InvalidKey:
            raise db.NonExistentUID(uid)
                    
    def write(utf8_content, preferred_uid=None):
        timestamp = time.time()
        if preferred_uid is None:
            uid = utils.make_uid(utf8_content, timestamp)
        else:
            uid = preferred_uid

        while uid in _db:
            uid = utils.refine_uid()
        _db[uid] = TextAndTimestamp(utf8_content, timestamp)
        return uid

