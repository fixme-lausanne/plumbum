import os
import sys
from os.path import dirname
sys.path.append(dirname(__file__))
#test of module choice should be done there
from db_memory import MemoryDB as cdb
import db
read = cdb.read
write = cdb.write
delete = cdb.delete
NonExistentUID = db.NonExistentUID

#from db_memory import MemoryDB as __module__
