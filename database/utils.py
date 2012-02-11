import hashlib
import random
import string


def make_uid(utf8_text, expiry_policy, _preferred_uid, timestamp):
    spec = ''.join((utf8_text, str(expiry_policy), str(timestamp)))
    return hashlib.sha1(spec.encode('utf-8')).hexdigest()


def refine_uid(uid):
    return str(uid) + random.choice(string.ascii_letters + string.digits)