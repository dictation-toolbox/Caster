import string, hashlib

from dragonfly import Text

from caster.lib import settings


def hash_password(text, text2, text3): 
    composite = str(text) + str(text) + str(text) + settings.SETTINGS["password"]["seed1"]
    hash_object = hashlib.sha256(composite)
    result = hash_object.hexdigest()[0:16]
    Text(result)._execute()

def get_password(text, text2, text3):
    base = settings.SETTINGS["password"]["seed1"] + str(string.lowercase.index(str(text)[0]) + 1) + str(string.lowercase.index(str(text2)[0]) + 1) + str(string.lowercase.index(str(text3)[0]) + 1)
    Text(base)._execute()

def get_restricted_password(text, text2, text3):
    base = settings.SETTINGS["password"]["seed2"] + str(string.lowercase.index(str(text)[0]) + 1) + str(string.lowercase.index(str(text2)[0]) + 1) + str(string.lowercase.index(str(text3)[0]) + 1)
    Text(base)._execute()

def get_simple_password(text, text2, text3):
    base = settings.SETTINGS["password"]["seed3"] + str(text)[0] + str(text2)[0] + str(text3)[0] + settings.SETTINGS["password"]["seed4"]
    Text(base)._execute()