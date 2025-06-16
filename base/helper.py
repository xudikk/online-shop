import base64
import binascii
import os


def code_decoder(code, decode=False, l=1):
    if decode:
        for i in range(l):
            code = base64.b64decode(code).decode()
        return code
    else:
        for i in range(l):
            code = base64.b64encode(str(code).encode()).decode()
        return code


def generate_key(size=50):
    return binascii.hexlify(os.urandom(size)).decode()




