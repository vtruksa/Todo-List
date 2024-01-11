import pbkdf2

from Crypto.Cipher import AES

def makePassword(password) -> bytes:
    p = pbkdf2.PBKDF2(password, salt=bytes(password, 'UTF-8')).read(256)
    return str(p)

def checkPassword(password, enc_password) -> bool:
    if makePassword(password) == enc_password: return True
    return False