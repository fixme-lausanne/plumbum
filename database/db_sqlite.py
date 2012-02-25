import json
import sqlite3
import database.api as api
import database.utils as utils
import db
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

class SqliteDB(db.DataBase):
    _DB = None

    def init(db_file="casket.sqlite"):
        SqliteDB._DB = sqlite3.Connection(db_file)
        
        
    @staticmethod
    def write(utf8_content, preferred_uid=None):
        if preferred_uid is None:
            uid = utils.make_uid(utf8_content)
        else:
            uid = preferred_uid
        SqliteDB._insert_json(uid, entry)
    
    @staticmethod
    def read():
        jentry = SqliteDB._retrieve_json(uid)
        if not jentry:
            raise db.NonExistentUID(uid)
        else:
            return json.loads(jentry.decode())

    def _retrieve_json(uid):
        sql_command = 
        jentry = SqliteDB.execute(sql_command)
        
    def _insert_json(uid, content):
        sql_command = 
        jentry = SqliteDB.execute(sql_command)
        
    def close():
        global db
        if KyotoDB._DB != None and not KyotoDB._DB.close():
            raise DataBaseError("close error: " + str(KyotoDB._DB.error()))
        db = None
