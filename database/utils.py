import hashlib


def make_uid(utf8_text, expiry_policy, _preferred_uid, timestamp):
    if _preferred_uid is None:
        _preferred_uid = ''
        uid_len = 8
    else:
        uid_len = len(_preferred_uid)
    spec = ''.join((utf8_text, str(expiry_policy), str(timestamp)))
    full_uid = _preferred_uid + hashlib.sha1(spec.encode('utf-8')).hexdigest()
    return (full_uid, uid_len)

