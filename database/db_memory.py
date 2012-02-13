from collections import namedtuple
from threading import Lock
import database.api as api
import database.utils as utils
import time

_db = {}
_lock = Lock()

TextAndTimestamp = namedtuple('TextAndTimestamp', 'text timestamp')


def post(utf8_text, expiry_policy=api.EXPIRY_NEVER, preferred_uid=None,
         _linked_uid_list=None):
    with _lock:
        timestamp = time.time()
        if preferred_uid is None:
            uid = utils.make_uid(utf8_text, expiry_policy,
                                 timestamp)
        else:
            uid = preferred_uid

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
