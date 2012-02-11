import time
import json
from hashlib import sha1
import kyotocabinet as kc
import pastebinlib.utils as utils

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
    check_db()
    if not db.close():
        raise DataBaseError("close error: " + str(db.error()))
    db = None

def check_db():
    if db == None:
        raise DataBaseError("database not open ")

def post(utf8_text,
        expiry_policy='NEVER',
        timeout=None,
        prefered_uid=None,
        linked_uid_list=None):
    check_db()
    if expiry_policy not in policies:
        raise ValueError("Policy %s is not in policies" % expiry_policy)
    entry = {}
    entry['utf8_text'] = utf8_text
    entry['expiry_policy'] = expiry_policy
    entry['timeout'] = str(timeout)
    entry['timestamp'] = str(time.time())
    if prefered_uid:
        hash_ = prefered_uid
    else:
        hash_ = utils.make_uid(utf8_text, expiry_policy, timeout
                , entry['timestamp'])[:8]
    jentry = json.dumps(entry)
    write_success = False
    while not write_success:
#TODO in theory, infinite loops can happen here
        write_success = db.add(hash_, jentry)
        hash_ = utils.refine_uid(hash_)[:8]
    return hash_

def retrieve_json(uid):
    check_db()
    jentry = db.get(uid)
    if not jentry:
        raise DataBaseError("get error: " + str(db.error()))
    else:
        return json.loads(jentry.decode())

def retrieve(uid):
    return retrieve_json(uid)['utf8_text']

def get_creation_timestamp(uid):
    return retrieve_json(uid)['timestamp']

def get_linked(uid):
    pass
