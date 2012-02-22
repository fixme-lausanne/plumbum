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
        pass
    
    @abstractmethod
    @staticmethod
    def write(utf8_content, preferred_uid=None):
        pass

    @staticmethod
    def _check_expiry(entry):
        timestamp = datetime.date.fromtimestamp(float(entry['timestamp']))
        now = datetime.date.fromtimestamp(time.time())
        policy = entry['expiry_policy']
        if policy == api.EXPIRY_HOUR_FROM_WRITE:
            return now - timestamp < datetime.timedelta(hours = 1)
        elif policy == api.EXPIRY_HOUR_FROM_READ:
            return now - timestamp < datetime.timedelta(hours = 1)
        elif policy == api.EXPIRY_WEEK_FROM_WRITE:
            return now - timestamp < datetime.timedelta(weeks = 1)
        elif policy == api.EXPIRY_WEEK_FROM_READ:
            return now - timestamp < datetime.timedelta(weeks = 1)
        else:
            return False


class NonExistentUID(Exception):
    def __init__(self, uid):
        self.uid = uid

    def __str__(self):
        return repr(self.uid)

class DataBaseError(Exception):
    pass
