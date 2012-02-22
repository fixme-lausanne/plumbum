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


def post(utf8_text, expiry_policy=EXPIRY_NEVER, prefered_uid=None,
         linked_uid_list=None):
    pass


def retrieve(uid):
    pass

def get_linked(uid):
    pass
