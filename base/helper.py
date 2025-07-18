import base64
import binascii
import os
import re


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


# Telefon raqami validatsiyasi
def validate_phone(phone):
    # O'zbekiston telefon raqami formati: +998XXYYYYYYY (12 ta belgi, +998 bilan boshlanadi)
    pattern = r'^\+998[0-9]{9}$'
    if re.match(pattern, phone):
        return True
    return False


# Email validatsiyasi
def validate_email(email):
    # Email formati: example@domain.com
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False

def dictfetchall(cursor):
    "cursordan kelayotgan tablitsa ichidagi barcha qatorlarni dict ko'rinishida qaytaradi"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    "cursordan kelayotgan tablitsa ichidagi bitta qatorni dict ko'rinishida qaytaradi"
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))




