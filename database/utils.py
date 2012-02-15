import hashlib
import random


def make_uid(utf8_text, expiry_policy, timestamp):
    spec = ''.join((utf8_text, str(expiry_policy), str(timestamp)))
    return hashlib.sha1(spec.encode('utf-8')).hexdigest()[:10]


def refine_uid():
    return ''.join([random.choice(string.ascii_lowercase + string.digits) for _
        in range(8)])

