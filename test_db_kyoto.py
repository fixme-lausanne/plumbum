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
dbk.post("test")
print(dbk.retrieve("ee229238"))
print(dbk.get_creation_timestamp("ee229238"))
dbk.bye()

