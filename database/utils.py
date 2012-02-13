import hashlib
import random
import string


def make_uid(utf8_text, expiry_policy, timestamp):
    spec = ''.join((utf8_text, str(expiry_policy), str(timestamp)))
    return hashlib.sha1(spec.encode('utf-8')).hexdigest()[:8]


def refine_uid():
    return ''.join([random.choice(string.ascii_letters + string.digits) for _
        in range(16)])
