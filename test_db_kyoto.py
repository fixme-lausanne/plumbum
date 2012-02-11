import pastebinlib.db_kyoto as dbk
from pastebinlib.api import NonExistentUID

try:
    dbk.post("test")
except dbk.DataBaseError:
    pass

try:
    dbk.retrieve("ee229238")
except NonExistentUID:
    pass

try:
    dbk.bye()
except dbk.DataBaseError:
    pass


dbk.init()
uid = dbk.post("test")
print(dbk.retrieve(uid))
print(dbk.get_creation_timestamp(uid))
uid_clash = dbk.post("a", preferred_uid="1")
uid_clahs1 = dbk.post("b", preferred_uid="1")
print(dbk.retrieve(uid_clash))
print(dbk.retrieve(uid_clahs1))

try:
    dbk.post("test", expiry_policy='NO_SUCH_POLICY')
except ValueError:
    pass

dbk.bye()
