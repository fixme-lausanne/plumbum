import os
import sys
from os.path import dirname, abspath
print(sys.path)
sys.path.append(dirname(abspath(__file__)))
#test of module choice should be done there

from api_method import post, retrieve, get_linked
from database import NonExistentUID
