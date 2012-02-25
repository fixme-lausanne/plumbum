import json
import sqlite3
import db
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
    
    @staticmethod
    def init(db_file="casket.sqlite"):
        SqliteDB._DB = sqlite3.Connection(db_file)
        
    @staticmethod
    def delete(uid):
        sql_command = 
        SqliteDB._DB.execute(sql_command)

    @staticmethod
    def write(utf8_content, preferred_uid=None):
        if preferred_uid is None:
            uid = utils.make_uid(utf8_content)
        else:
            uid = preferred_uid
        while SqliteDB._retrieve_json(uid):
            uid = utils.refine_uid()
        SqliteDB._insert_json(uid, entry)
    
    @staticmethod
    def read():
        jentry = SqliteDB._retrieve_json(uid)
        if not jentry:
            raise db.NonExistentUID(uid)
        else:
            return json.loads(jentry.decode())
    
    @staticmethod
    def _retrieve_json(uid):
        sql_command = 
        jentry = SqliteDB.execute(sql_command)
    
    @staticmethod
    def _insert_json(uid, content):
        sql_command = 
        jentry = SqliteDB.execute(sql_command)
    
    @staticmethod
    def close():
        SqliteDB._DB.close()
