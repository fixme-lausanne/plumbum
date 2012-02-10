import sys
import time
import json
from hashlib import sha1
import kyotocabinet as kc

policies = ['NEVER', 'AFTER_READ']
db = None

def init():
    # create the database object
    global db
    db = kc.DB()
    # open the database
    if not db.open("casket.kch", kc.DB.OWRITER | kc.DB.OCREATE):
        print("open error: " + str(db.error()), file=sys.stderr)

def bye():
    # close the database
    if not db.close():
        print("close error: " + str(db.error()), file=sys.stderr)


def post(utf8_text,
        expiry_policy='NEVER',
        timeout=None,
        prefered_uid=None,
        linked_uid_list=None):
    # must add a timestap too
    entry = {}
    entry['utf8_text'] = utf8_text
    entry['expiry_policy'] = expiry_policy
    entry['timeout'] = str(timeout)
    entry['timestamp'] = str(time.time())
    hash_ = sha1(("".join(entry.values())).encode("utf-8")).hexdigest()[:8]
    jentry = json.dumps(entry)
    db.set(hash_, jentry)

def retrieve(uid):
    jentry = db.get(uid).decode()
    return json.loads(jentry)

def get_creation_timestamp(uid):
    return retrieve(uid)['timestamp']

def get_linked(uid):
    pass
