from cryptography.hazmat.primitives.ciphers.modes import CBC
flag1 = ''
flag2 = 'bbb'
key = b'a' * 16
iv = b'a' * 16
mode = CBC(iv)
