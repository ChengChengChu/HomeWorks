from pwn import *
import random
from exploit import *
from cryptoFunc import *

flag1 = b'CNS{Aka_BIT_f1ipp1N9_atTaCk!}'

JOB_TITLE = 'Grand Disciplinary Officer'
NAME = 'Azar'

info = f'job title:{JOB_TITLE}||name:{NAME}||secret word:{flag1.decode()}'.encode()   

def recv_to_send_guess(p) :
    p.recvuntil(b'choice: ')
    p.sendline('1'.encode())
    p.recvuntil(b'(hex encoded): ')
    
    return

def guess_cipher(cipher, tmp) :
    ret = ''
    # to 32
    for i in range(32) :
        ret += cipher[i]
    # print(tmp)
    # tmp = f"0x{tmp:02x}".replace('0x', '')
    # print(tmp, type(tmp))
    for i in range(len(tmp)) :
        t = tmp[i]
        t = f"0x{t:02x}".replace('0x', '')

        ret += t

    for i in range(40, len(cipher)) :
        ret += cipher[i]
    
    # print(len(cipher), len(ret))
    assert (len(cipher) == len(ret))
    
    return ret

    # print(tmp, '\n\n')
    for i in range(len(tmp)) :
        t = tmp[i]
        t = f"0x{t:02x}"
        ret += t.replace('0x', '')

    for i in range(40, len(cipher)) :
        ret += cipher[i]


    return ret

def _decode(c, X) :
    foo = bytearray(b'')
    for i in range(1, 6) :
        for j in range(16) :
            tmp = bytes_to_long(c[i-1][j]) ^ X[i][j]
            # tmp = long_to_bytes(tmp)
            foo.append(tmp)
    
    return foo
### need to modify block[1][0, 1, 2, 3]

def main() :
    X = [[], [52, 89, 236, 251, 12, 78, 235, 182, 238, 35, 17, 172, 128, 123, 233, 119], [53, 85, 217, 14, 80, 161, 144, 99, 146, 177, 127, 107, 113, 88, 90, 60], [52, 102, 136, 239, 125, 113, 217, 172, 204, 222, 181, 216, 40, 252, 111, 33], [36, 224, 55, 111, 36, 225, 111, 176, 108, 138, 112, 180, 138, 132, 44, 105], [147, 71, 175, 55, 213, 199, 94, 115, 95, 182, 218, 207, 114, 1, 65, 213]]

    c = [[b'p', b'0', b'\x9f', b'\x98', b'e', b'>', b'\x87', b'\xdf', b'\x80', b'B', b'c', b'\xd5', b'\xa0', b'4', b'\x8f', b'\x11'], [b'\\', b'6', b'\xbc', b'|', b',', b'\xdd', b'\xfe', b'\x02', b'\xff', b'\xd4', b'E', b'(', b'\x08', b'6', b'5', b'@'], [b'H', b'\x15', b'\xed', b'\x8c', b'\x0f', b'\x14', b'\xad', b'\x8c', b'\xbb', b'\xb1', b'\xc7', b'\xbc', b'\x12', b'\xbf', b'!', b'r'], [b'_', b'\xa1', b'\\', b'\x0e', b'{', b'\xa3', b'&', b'\xe4', b'3', b'\xec', b'A', b'\xdd', b'\xfa', b'\xf4', b'\x1d', b"'"], [b'\xaa', b'\x18', b'\xce', b'C', b'\x81', b'\xa6', b'\x1d', b'\x18', b'~', b'\xcb', b'\xdc', b'\xc9', b't', b'\x07', b'G', b'\xd3'], [b'\x00', b'\xb7', b'\xf3', b'T', b'\xbb', b'h', b'\x13', b'\x9f', b'#', b'\x06', b'P', b'\x8a', b'\x06', b'\xa0', b'O', b'\xbe']]
    
    my_plain = [[106, 111, 98, 32, 116, 105, 116, 108, 101, 58, 71, 114, 97, 110, 100, 32], [68, 105, 115, 99, 105, 112, 108, 105, 110, 97, 114, 121, 32, 79, 102, 102], [105, 99, 101, 114, 124, 124, 110, 97, 109, 101, 58, 65, 122, 97, 114, 124], [124, 115, 101, 99, 114, 101, 116, 32, 119, 111, 114, 100, 58, 67, 78, 83], [123, 65, 107, 97, 95, 66, 73, 84, 95, 102, 49, 105, 112, 112, 49, 78], [57, 95, 97, 116, 84, 97, 67, 107, 33, 125, 6, 6, 6, 6, 6, 6]]
    
    


    p = remote('cns.csie.org', 44399)
    # p = process(['python3', 'server.py'])
    p.recvuntil(b'ID: ')
    ID = p.recvuntil(b'----+', drop=True).decode().replace('\n', '').replace('-', '').replace('+', '').replace('|', '').replace(' ', '')
    p.recvuntil(b'our choice: ')
    p.sendline('2'.encode())
    p.recvuntil(b'Your choice: ')
    p.sendline('3'.encode())
    p.recvuntil(b'choice: ')
    p.sendline('1'.encode())
    p.recvuntil(b"word: ")
    p.sendline(flag1)
    
    print(len(c), len(X), len(my_plain))
    
    cipher = '' 
    
    ### 11, 12, 13, 14 ###
    modify = [long_to_bytes(x^y) for (x, y) in  zip(X[2][11:15], my_plain[2][11:15])]

    for i in range(11, 15) :
        c[1][i] = modify[i - 11]
    
    # foo = bytearray(b'')
    # for i in range(1, 6) :
    #     for j in range(16) :
    #         tmp = bytes_to_long(c[i-1][j]) ^ X[i][j]
            # tmp = long_to_bytes(tmp)
    #         foo.append(tmp)
    
    # print(foo)
    foo = _decode(c, X)
    # print(foo)
    
    _ = []
    idx = 0
    ## change block2 0, 1, 2, 3##
    while idx < 256 :
        
        cipher = ''
        my_guess = [0, 0, 45, 66]
        # for i in range(2) :
        #     my_guess.append(random.randint(0, 255))
        idx += 1
        for i in range(4) :
            c[1][i] = long_to_bytes(my_guess[i])

        for i in range(6) :
            tmp = []
            for j in range(16) :
                if True:
                    a = bytes_to_long(c[i][j])
                    cipher += f'0x{a:02x}'.replace('0x', '')
        
        # print(len(cipher))
        foo = _decode(c, X)
        foo = bytes(foo)
        foo = unpad(foo).decode()
        print(f"{foo}, {idx}")
        try :
            foo = foo.decode()
            print(foo)
            _.append(idx - 1)
        except :
            # break
            continue
        # print(cipher)
        # p.interactive()
        if True : 
            # foo = foo.decode()
            # print('\n', foo)
            # print(cipher, '\n')
            recv_to_send_guess(p)
            p.sendline(cipher.encode())
            msg = p.recvuntil(b'\n', drop=True).decode()
            # print(msg)
            # print(my_guess)
            # print(len(_))
            # breai
        print(msg)
        # except :
        #     continue
        # recv_to_send_guess(p)
        # p.sendline(cipher.encode())
        # msg = p.recvuntil(b'\n', drop=True).decode()
        # print(msg)
        # p.interactive()
        if idx % 1000 == 0 : print(f"guess {idx} times")
        if msg[0] != 'A' : 
            print(msg)
            break
    # print(f"cipher : {cipher}", len(cipher))
    # print(f"after guess : {_}", len(_))

if __name__ == "__main__" :
    main()
