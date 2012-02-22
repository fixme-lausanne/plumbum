import datetime
import time
import json
import kyotocabinet as kc
import database.api as api
import database.utils as utils

""" Interact with Kyoto Cabinet

Example
-------

import db_kyoto as dbk
dbk.init()
uid = dbk.post("test")
print(dbk.retrieve(uid))

Notes
-----

All db access methods will raise a DataBaseError if they don't succeed.
Thus you should enclose them in a try-except like:

try:
    uid = dbk.post("test")
except DataBaseError
    pass

The database connection is lazy, if it does not exist, it will be attempted.

TODO
----
linked_uid_list is not implemented
"""

db = None

class DataBaseError(Exception):
    pass


def init(db_file="casket.kch"):
    global db
    db = kc.DB()
    if not db.open(db_file, kc.DB.OWRITER | kc.DB.OCREATE):
        raise DataBaseError("open error: " + str(db.error()))


def post(utf8_text,
        expiry_policy=api.EXPIRY_NEVER,
        preferred_uid=None,
        linked_uid_list=None):
    _check_db()
    if expiry_policy not in api.expiry_policies:
        raise ValueError("Policy %s is not in policies" % expiry_policy)
    entry = {}
    entry['utf8_text'] = utf8_text
    entry['expiry_policy'] = expiry_policy
    entry['timestamp'] = str(time.time())
    entry['read_timestamp'] = None;
    if preferred_uid is None:
        hash_ = utils.make_uid(utf8_text, expiry_policy, entry['timestamp'])
    else:
        hash_ = preferred_uid

    jentry = json.dumps(entry)
    write_success = db.add(hash_, jentry)
    while not write_success:
        hash_ = utils.refine_uid()
        write_success = db.add(hash_, jentry)
    return hash_

def retrieve(uid):
    entry = _retrieve_json(uid)
    now = time.time()
    if entry['read_timestamp'] is None:
        entry['read_timestamp'] = str(now)
    if _check_expiry(entry):
        db.remove(uid)
        raise api.NonExistentUID
    else:
        if entry['read_timestamp'] == now:
            jentry = json.dumps(entry)
            #TODO check if write succeeded
            write_success = db.set(uid, jentry)
        return entry['utf8_text']

def get_creation_timestamp(uid):
    return _retrieve_json(uid)['timestamp']

def get_linked(uid):
    pass

def bye():
    global db
    if db !=None and not db.close():
        raise DataBaseError("close error: " + str(db.error()))
    db = None

def _retrieve_json(uid):
    _check_db()
    jentry = db.get(uid)
    if not jentry:
        raise api.NonExistentUID(uid)
    else:
        return json.loads(jentry.decode())

def _check_db():
    if db == None:
        init()

def _check_expiry(entry):
    read_timestamp = datetime.date.fromtimestamp(float(entry['read_timestamp']))
    write_timestamp = datetime.date.fromtimestamp(float(entry['timestamp']))
    now = datetime.date.fromtimestamp(time.time())
    policy = entry['expiry_policy']
    if policy == api.EXPIRY_HOUR_FROM_WRITE:
        return now - write_timestamp < datetime.timedelta(hours = 1)
    elif policy == api.EXPIRY_HOUR_FROM_READ:
        return now - read_timestamp < datetime.timedelta(hours = 1)
    elif policy == api.EXPIRY_WEEK_FROM_WRITE:
        return now - write_timestamp < datetime.timedelta(weeks = 1)
    elif policy == api.EXPIRY_WEEK_FROM_READ:
        return now - read_timestamp < datetime.timedelta(weeks = 1)
    else:
        return False

