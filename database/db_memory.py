from collections import namedtuple
from threading import Lock as TLock
from multiprocessing import Lock as PLock
import utils as utils
import time
import db
"""Just an abstract class for a database"""

class MemoryDB(db.DataBase):

    _DB = dict()
    _TLOCK = TLock()
    _PLOCK = PLock()
    TextAndTimestamp = namedtuple('TextAndTimestamp', 'text timestamp')
    
    @staticmethod
    def init():
        MemoryDB._DB = dict()
        
    @staticmethod
    def delete(uid):
        with MemoryDB._PLOCK and MemoryDB._TLOCK:
            del MemoryDB._DB[uid]
    
    @staticmethod
    def read(uid):
        with MemoryDB._PLOCK and MemoryDB._TLOCK:
            try:
                return MemoryDB._DB[uid]
            except KeyError:
                raise db.NonExistentUID(uid)
    
    @staticmethod
    def write(utf8_content, preferred_uid=None):
        with MemoryDB._PLOCK and MemoryDB._TLOCK:
            timestamp = time.time()
            if preferred_uid is None:
                uid = utils.make_uid(utf8_content, timestamp)
            else:
                uid = preferred_uid
            while uid in MemoryDB._DB:
                uid = utils.refine_uid()
            MemoryDB._DB[uid] = utf8_content
            return uid
    
    @staticmethod
    def _get_entry(uid):
        try:
            return MemoryDB._DB[uid]
        except KeyError :
            raise db.NonExistentUID(uid)
