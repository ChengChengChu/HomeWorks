from Crypto.Cipher import AES
from myErrors import *
import binascii
import secret


def pad(m):
    length = 16-len(m) % 16
    # print("Debug INFO : pad")
    # print(f"length : {length}")
    # print(f"padding value : {chr(length).encode()}")
    # print(f"message after pad : {m+chr(length).encode()*length}")
    return m+chr(length).encode()*length

def unpad(c):
    length = c[-1]
    
    # print('\n\n', c, '\n\n')
    # print(f"\n\nlength : {length}\n\n")
    for char in c[-length:]:
        if char != length:
            flag = False
            # print(f"incorrect padding, last byte : {char}, correct paddig is {length}")
            # brea
            # print("PADDING ERROR")
            # break
            raise paddingError('incorrect padding')

    if False :
        print(f"INFO : Correct padding, last byte is {length}")
        
    return c[:-length]# , flag


def encrypt(m):
    aes = AES.new(secret.key, AES.MODE_CBC, secret.iv)
    
    return binascii.hexlify(aes.encrypt(pad(m))).decode()


def decrypt(c):
    aes = AES.new(secret.key, AES.MODE_CBC, secret.iv)
    # tmp=  unpad(aes.decrypt(binascii.unhexlify(c)).decode())
    return unpad(aes.decrypt(binascii.unhexlify(c))).decode()
    # print(f"decode message : {tmp}\n\n")
    # return tmp
