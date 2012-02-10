import time
import json
from hashlib import sha1
import kyotocabinet as kc

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

TODO
----
prefered_uid is not implemented
linked_uid_list is not implemented

"""

policies = ['NEVER', 'AFTER_READ']
db = None

class DataBaseError(Exception):
    pass

def init(db_file="casket.kch"):
    global db
    db = kc.DB()
    if not db.open(db_file, kc.DB.OWRITER | kc.DB.OCREATE):
        raise DataBaseError("open error: " + str(db.error()))

def bye():
    global db
    if not db.close():
        raise DataBaseError("close error: " + str(db.error()))
    db = None

def check_db():
    if not db:
        raise DataBaseError("database not open ")

def post(utf8_text,
        expiry_policy='NEVER',
        timeout=None,
        prefered_uid=None,
        linked_uid_list=None):
    check_db()
    entry = {}
    entry['utf8_text'] = utf8_text
    entry['expiry_policy'] = expiry_policy
    entry['timeout'] = str(timeout)
    entry['timestamp'] = str(time.time())
    hash_ = sha1(("".join(entry.values())).encode("utf-8")).hexdigest()[:8]
    jentry = json.dumps(entry)
    db.set(hash_, jentry)
    return hash_

def retrieve(uid):
    check_db()
    jentry = db.get(uid)
    if not jentry:
        raise DataBaseError("get error: " + str(db.error()))
    else:
        return json.loads(jentry.decode())

def get_creation_timestamp(uid):
    return retrieve(uid)['timestamp']

def get_linked(uid):
    pass
