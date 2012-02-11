from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
import pastebinlib.db_kyoto as dbk
import logging
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
logging.debug(dbk.retrieve(uid))
logging.debug(dbk.get_creation_timestamp(uid))
uid_clash = dbk.post("a", preferred_uid="1")
uid_clahs1 = dbk.post("b", preferred_uid="1")
logging.debug(dbk.retrieve(uid_clash))
logging.debug(dbk.retrieve(uid_clahs1))

try:
    dbk.post("test", expiry_policy='NO_SUCH_POLICY')
except ValueError:
    pass

dbk.bye()
