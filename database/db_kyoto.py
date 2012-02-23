import time
import json
import kyotocabinet as kc
import database.api as api
import database.utils as utils
from db import DataBase

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
class KyotoDB(db.DataBase):
    _DB = None

    def init(db_file="casket.kch"):
        global db
        KyotoDB._DB = kc.DB()
        if not db.open(db_file, kc.DB.OWRITER | kc.DB.OCREATE):
            raise db.DataBaseError("open error: " + str(db.error()))
            
    def delete(uid):
        pass
    def read(uid):
        pass
        
    def write(utf8_content, preferred_uid=None):
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
        KyotoDB._DB[hash_] = entry
        
    def close():
        global db
        if KyotoDB._DB != None and not KyotoDB._DB.close():
            raise DataBaseError("close error: " + str(KyotoDB._DB.error()))
        db = None

    def _retrieve_json(uid):
        _check_db()
        jentry = db.get(uid)
        if not jentry:
            raise db.NonExistentUID(uid)
        else:
            return json.loads(jentry.decode())

    def _check_db():
        if db == None:
            init()
