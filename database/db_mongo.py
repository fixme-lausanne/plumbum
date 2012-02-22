from collections import namedtuple
from threading import Lock as TLock
import database.api as api
import database.utils as utils
import time
import pymongo

_db = None
TLOCK = TLock()
TextAndTimestamp = namedtuple('TextAndTimestamp', 'text timestamp')

def init():
    _db = Connection('localhost', 27017)
    
def post(utf8_text, expiry_policy=api.EXPIRY_NEVER, prefered_uid=None,
         _linked_uid_list=None):
    with TLOCK:
        timestamp = time.time()
        if prefered_uid is None:
            uid = utils.make_uid(utf8_text, expiry_policy,
                                 timestamp)
        else:
            uid = prefered_uid

        while uid in _db:
            uid = utils.refine_uid()
        _db[uid] = TextAndTimestamp(utf8_text, timestamp)
        return uid


def retrieve(uid):
    return _get_entry(uid).text


def get_creation_timestamp(uid):
    return _get_entry(uid).timestamp


def get_linked(uid):
    raise NotImplemented()


def _get_entry(uid):
    try:
        return _db[uid]
    except KeyError:
        raise api.NonExistentUID(uid)
