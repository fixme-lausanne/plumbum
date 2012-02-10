import db_kyoto as dbk

try:
    dbk.post("test")
except dbk.DataBaseError:
    pass

try:
    dbk.retrieve("ee229238")
except dbk.DataBaseError:
    pass

dbk.init()
uid = dbk.post("test")
print(dbk.retrieve(uid))
print(dbk.get_creation_timestamp(uid))
#dbk.bye()

