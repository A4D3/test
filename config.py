import os, binascii
class Config(object):
    SECRET_KEY = binascii.hexlify(os.urandom(24))
