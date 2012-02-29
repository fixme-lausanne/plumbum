import os
import sys
from os.path import dirname
sys.path.append(dirname(__file__))
#test of module choice should be done there
from db_memory import MemoryDB as db
read = db.read
write = db.write
delete = db.delete

#from db_memory import MemoryDB as __module__
