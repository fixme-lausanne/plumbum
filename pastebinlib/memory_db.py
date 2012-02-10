import pastebinlib.api as api
import pastebinlib.utils as utils

from collections import namedtuple
import time
_db = {}

TextAndTimestamp = namedtuple('TextAndTimestamp', 'text timestamp')


def post(utf8_text, expiry_policy=api.EXPIRY_NEVER, timeout=0, prefered_uid=None, _linked_uid_list=None):
    uid = utils.make_uid(utf8_text)
    while uid in _db:
        uid = utils.refine_uid(uid)
    _db[uid] = TextAndTimestamp(utf8_text, time.time())


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