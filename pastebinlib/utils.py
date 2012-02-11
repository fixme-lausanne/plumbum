import hashlib
import random
import string

try:
    letters = string.ascii_letters
except AttributeError:
    letters = string.letters

def make_uid(utf8_text, expiry_policy, timeout, _preferred_uid, timestamp):
    spec = ''.join((utf8_text, str(expiry_policy), str(timeout), str(timestamp)))
    return hashlib.sha1(spec.encode('utf-8')).hexdigest()

def refine_uid(uid):
    return str(uid) + random.choice(letters + string.digits)
