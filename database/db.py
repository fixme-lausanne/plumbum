from abc import abstractmethod, ABCMeta
from collections import namedtuple

TextAndTimestamp = namedtuple('TextAndTimestamp', 'text timestamp')

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
        pass
    
    @abstractmethod
    @staticmethod
    def write(utf8_content, preferred_uid=None):
        pass


class NonExistentUID(Exception):
    def __init__(self, uid):
        self.uid = uid

    def __str__(self):
        return repr(self.uid)

class DataBaseError(Exception):
    pass
