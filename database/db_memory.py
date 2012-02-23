from collections import namedtuple
from threading import Lock as TLock
from multiprocessing import Lock as PLock
import database.api as api
import database.utils as utils
import db
import time

class MemoryDB(db.DataBase):

    _DB = {}
    _TLOCK = TLock()
    _PLOCK = PLock()
    TextAndTimestamp = namedtuple('TextAndTimestamp', 'text timestamp')
from abc import abstractmethod, ABCMeta

"""Just an abstract class for a database"""
class DataBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    @staticmethod
    def delete(uid):
        pass
        
    @abstractmethod
    @staticmethod
    def read(uid):
        with MemoryDB._PLOCK and MemoryDB._TLOCK:
            try:
                return MemoryDB._DB['uid']
            except KeyError:
                raise db.NonExistentUID(uid)

    
    @abstractmethod
    @staticmethod
    def write(utf8_content, preferred_uid=None):
        with MemoryDB.PLock and MemoryDB.TLOCK:
            timestamp = time.time()
            if preferred_uid is None:
                uid = utils.make_uid(utf8_content, timestamp)
            else:
                uid = preferred_uid

            while uid in MemoryDB._DB:
                uid = utils.refine_uid()
            MemoryDB._DB[uid] = db.TextAndTimestamp(utf8_content, timestamp)
            return uid

    def _get_entry(uid):
        try:
            return MemoryDB._DB[uid]
        except KeyError :
            raise api.NonExistentUID(uid)
