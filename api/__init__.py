import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import api 
post = api.post
retrieve = api.retrieve
NonExistentUID = api.NonExistentUID
