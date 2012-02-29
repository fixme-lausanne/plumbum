from os.path import dirname, abspath, join
import sys
sys.path.append(join(dirname(dirname(abspath(__file__))), "database"))

#TODO import and test DBs

from db_memory import MemoryDB as db
import time
import datetime

EXPIRY_NEVER = 1
EXPIRY_HOUR_FROM_READ = 2
EXPIRY_HOUR_FROM_WRITE = 3
EXPIRY_WEEK_FROM_READ = 4
EXPIRY_WEEK_FROM_WRITE = 5

expiry_policies = (EXPIRY_NEVER, EXPIRY_WEEK_FROM_READ, EXPIRY_WEEK_FROM_WRITE,
        EXPIRY_HOUR_FROM_READ, EXPIRY_HOUR_FROM_WRITE)


class NonExistentUID(Exception):
    def __init__(self, uid):
        self.uid = uid

    def __str__(self):
        return repr(self.uid)


def post(utf8_text, expiry_policy=EXPIRY_NEVER, prefered_uid=None,linked_uid_list=None):
    if expiry_policy not in expiry_policies:
        raise ValueError("Policy %s is not in policies" % expiry_policy)
    entry = {}
    entry['text'] = utf8_text
    entry['expiry_policy'] = expiry_policy
    entry['timestamp'] = str(time.time())
    entry['read_timestamp'] = None
    entry['linked'] = linked_uid_list
    db.write(entry, prefered_uid)


def retrieve(uid):
    entry = db.read(uid)
    if _is_expired(entry):
        db.delete(uid)
        raise NonExistentUID(uid)
    else:
        return entry['text']

def get_linked(uid):
    entry = db.read(uid)
    return entry['linked']

def _is_expired(entry):
    timestamp = datetime.date.fromtimestamp(float(entry['timestamp']))
    now = datetime.date.fromtimestamp(time.time())
    policy = entry['expiry_policy']
    if policy == EXPIRY_HOUR_FROM_WRITE:
        return now - timestamp < datetime.timedelta(hours = 1)
    elif policy == EXPIRY_HOUR_FROM_READ:
        return now - timestamp < datetime.timedelta(hours = 1)
    elif policy == EXPIRY_WEEK_FROM_WRITE:
        return now - timestamp < datetime.timedelta(weeks = 1)
    elif policy == EXPIRY_WEEK_FROM_READ:
        return now - timestamp < datetime.timedelta(weeks = 1)
    else:
        return False
