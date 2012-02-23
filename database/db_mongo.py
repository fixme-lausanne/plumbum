import database.utils as utils
import time
import pymongo
import db

class MongoDB(db.DataBase):
    _DBConn = pymongo.Connection('localhost', 27017)
    _DB = _DBConn['plumbum']
    
    def delete(uid):
        MongoDB._DB.remove(uid)
        
    def read(uid):
        try:
            MongoDB.DB.get(uid)
        except KeyError:
            raise db.NonExistentUID(uid)
                    
    def write(utf8_content, preferred_uid=None):
        timestamp = time.time()
        if preferred_uid is None:
            uid = utils.make_uid(utf8_content, timestamp)
        else:
            uid = preferred_uid

        while uid in _db:
            uid = utils.refine_uid()
        MongoDB._DB[uid] = TextAndTimestamp(utf8_content, timestamp)
        return uid

