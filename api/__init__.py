import os
import sys
from os.path import dirname, abspath
print(sys.path)
sys.path.append(dirname(abspath(__file__)))
#test of module choice should be done there

import api
#from db_memory import MemoryDB as __module__
