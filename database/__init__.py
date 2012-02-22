import sys
import logging
from database.api import NonExistentUID

try:
    from database.db_kyoto import post, retrieve
    print("Using Kyoto Cabinet, baby!")
except ImportError:
    logging.error('Cannot import kyoto db, falling back to memory db \
(reason for failure: %s )' % sys.exc_info()[0])
    from  database.db_memory import post, retrieve
