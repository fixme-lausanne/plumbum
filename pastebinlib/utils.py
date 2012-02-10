import hashlib
import random
import string


def make_uid(content):
    return hashlib.md5(content).hexdigest()


def refine_uid(uid):
    return str(uid) + random.choice(string.letters + string.digits)
