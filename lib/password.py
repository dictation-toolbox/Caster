import string, hashlib

from dragonfly import Text

from lib import settings


def hash_password(text, text2, text3): 
    composite = str(text) + str(text) + str(text) + settings.PBASE1
    hash_object = hashlib.sha256(composite)
    result = hash_object.hexdigest()[0:16]
    Text(result)._execute()

def get_password(text, text2, text3):
    base = settings.PBASE1 + str(string.lowercase.index(str(text)[0]) + 1) + str(string.lowercase.index(str(text2)[0]) + 1) + str(string.lowercase.index(str(text3)[0]) + 1)
    Text(base)._execute()

def get_restricted_password(text, text2, text3):
    base = settings.PBASE2 + str(string.lowercase.index(str(text)[0]) + 1) + str(string.lowercase.index(str(text2)[0]) + 1) + str(string.lowercase.index(str(text3)[0]) + 1)
    Text(base)._execute()

def get_simple_password(text, text2, text3):
    base = settings.PBASE3 + str(text)[0] + str(text2)[0] + str(text3)[0] + settings.PBASE4
    Text(base)._execute()