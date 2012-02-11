import pastebinlib.db_kyoto as dbk

try:
    dbk.post("test")
except dbk.DataBaseError:
    pass

try:
    dbk.retrieve("ee229238")
except dbk.DataBaseError:
    pass

try:
    dbk.bye()
except dbk.DataBaseError:
    pass


dbk.init()
uid = dbk.post("test")
print(dbk.retrieve_json(uid))
print(dbk.retrieve(uid))
print(dbk.get_creation_timestamp(uid))
uid_clash = dbk.post("a", prefered_uid="1")
uid_clahs1 = dbk.post("b", prefered_uid="1")
print(dbk.retrieve(uid_clash))
print(dbk.retrieve(uid_clahs1))

try:
    dbk.post("test", expiry_policy='NO_SUCH_POLICY')
except ValueError:
    pass

dbk.bye()
