import hashlib
import random
import string

try:
    rng = random.SystemRandom()
except NotImplementedError:
    #fallback if the system doesn't have a random number generator
    rng = random.Random()

def make_uid(*args):
    spec = ''.join([str(arg) for arg in args])
    return hashlib.sha1(spec.encode('utf-8')).hexdigest()[:10]


def refine_uid():
    return ''.join(rng.choice(string.ascii_lowercase + string.digits) for _
        in range(8))

