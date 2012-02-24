import utils as utils
import time
import pymongo
import db

class MongoDB(db.DataBase):
    _DB = pymongo.Connection('localhost', 27017)['plumbum']['plumbum']
    
    @staticmethod
    def init():
        MongoDB._DB.create_index('key')
        
    @staticmethod
    def delete(uid):
        MongoDB._DB.drop_collection(uid)

    @staticmethod
    def read(uid):
        try:
            return MongoDB._DB[uid]
        except KeyError:
            raise db.NonExistentUID(uid)
    
    @staticmethod
    def write(utf8_content, preferred_uid=None):
        timestamp = time.time()
        if preferred_uid is None:
            uid = utils.make_uid(utf8_content, timestamp)
        else:
            uid = preferred_uid
        print(dir(MongoDB._DB))
        while MongoDB._DB.find(uid):
            uid = utils.refine_uid()
        MongoDB._DB.create_collection(uid)
        print(dir(MongoDB._DB))
        MongoDB._DB.uid.insert(utf8_content)
        return uid

