import kyotocabinet as kc
import sys

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
    pass

def retrieve(uid):
    pass

def get_creation_timestamp(uid):
    pass

def get_linked(uid):
    pass
