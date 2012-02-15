from collections import namedtuple
from threading import Lock as TLock
import database.api as api
import database.utils as utils
import time

_db = {}
TLOCK = TLock()
TextAndTimestamp = namedtuple('TextAndTimestamp', 'text timestamp')


def post(utf8_text, expiry_policy=api.EXPIRY_NEVER, prefered_uid=None,
         _linked_uid_list=None):
    with TLOCK:
        timestamp = time.time()
        full_uid, uid_len = utils.make_uid(utf8_text, expiry_policy,
                             prefered_uid, timestamp)
        uid = full_uid[:uid_len]
        while uid in _db:
            uid_len += 1
            uid = full_uid[:uid_len]
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
