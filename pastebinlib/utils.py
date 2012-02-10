import md5
import random
import string


def make_uid(content):
    return md5.new(content).digest()


def refine_uid(uid):
    return str(uid) + random.choice(string.letters + string.digits)