EXPIRY_NEVER = 1
EXPIRY_FROM_READ = 2
EXPIRY_FROM_WRITE = 3


class NonExistentUID(Exception):
    def __init__(self, uid):
        self.uid = uid

    def __str__(self):
        return repr(self.uid)


def post(utf8_text, expiry_policy=EXPIRY_NEVER, timeout=0, prefered_uid=None, 
         linked_uid_list=None):
    pass


def retrieve(uid):
    pass


def get_creation_timestamp(uid):
    pass


def get_linked(uid):
    pass
