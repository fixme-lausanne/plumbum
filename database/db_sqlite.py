import sqlite3
import db
import utils

def test_init(f):
    def wrapper(*args, **kw):
        if SqliteDB._DB == None:
            SqliteDB.init()
        return f(*args, **kw)
    return wrapper

class SqliteDB(db.DataBase):
    _DB = None
    
    @staticmethod
    def init(db_file="casket.sqlite"):
        SqliteDB._DB = sqlite3.Connection(db_file)
        #init table for key/value use
        SqliteDB._DB.execute("""CREATE TABLE IF NOT EXISTS PASTE (
        UID         VARCHAR (10)      NOT NULL,
        JSON        VARCHAR           NOT NULL)""")
            
    @staticmethod
    @test_init
    def delete(uid):
        sql_command = "DROP UID"
        SqliteDB._DB.execute(sql_command)
    
    @staticmethod
    @test_init
    def write(utf8_content, preferred_uid=None):
        if preferred_uid is None:
            uid = utils.make_uid(utf8_content)
        else:
            uid = preferred_uid
        while SqliteDB._retrieve_json(uid):
            uid = utils.refine_uid()
        SqliteDB._insert_json(uid, utf8_content)
        return uid

    @staticmethod
    @test_init
    def read(uid):
        jentry = SqliteDB._retrieve_json(uid)
        if not jentry:
            raise db.NonExistentUID(uid)
        else:
            return jentry
    
    @staticmethod
    @test_init
    def _retrieve_json(uid):
        sql_command = "SELECT JSON FROM PASTE WHERE UID=?;"
        c = SqliteDB._DB.cursor()
        c.execute(sql_command, [uid])
        st = c.fetchone()
        if st:
            return st[0]
        else: 
            return None
    
    @staticmethod
    @test_init
    def _insert_json(uid, content):
        sql_command = "INSERT INTO PASTE (UID, JSON) VALUES (?, ?)"
        c = SqliteDB._DB.cursor()
        c.execute(sql_command, [uid, content])
        SqliteDB._DB.commit()
    
    @staticmethod
    def close():
        SqliteDB._DB.execute("DROP TABLE IF EXISTS PASTE")
        SqliteDB._DB.close()
        SqliteDB._DB = None
