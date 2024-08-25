import base64
import hashlib
from yaml import dump


def encode(num: str):
    hasher = hashlib.sha1(num.encode())
    return str(base64.urlsafe_b64encode(hasher.digest()))[2:10]


def identifier(obj: object):
    return encode(dump(obj))
