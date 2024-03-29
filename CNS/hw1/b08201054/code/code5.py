from pwn import *
import time 
import random
import base64
from utils import *
import warnings  

words = []
get_flag = False
with open('common_words.txt', 'r') as fp :
    for line in fp.read().splitlines() :
        words.append(line)

def start():
    _r = remote("cns.csie.org", 44398)
    return _r


def decode_ceaser(text) :
    for offset in range(50) :
        decode = ""
        for x in text :
            if ord(x) >= 97 and ord(x) <= 122 :
                decode += chr((ord(x) + offset - 97) % 26 + 97)
            elif ord(x) >= 65 and ord(x) <= 90 :
                decode += chr((ord(x) + offset - 65) % 26 + 65)
            else :
                decode += x
        count = 0
        for d in decode.split() :
            for w in words :
                if d == w :
                   #  print(d)
                    count += 1
        if count >= 1 :
            # print("========\n", decode, "========\n")
            return decode

    return "Not enough common_words"
def decode_fence(cipher, key) :
        rail = [['\n' for i in range(len(cipher))]
                                for j in range(key)]

        dir_down = None
        row, col = 0, 0

        for i in range(len(cipher)):
                if row == 0:
                        dir_down = True
                if row == key - 1:
                        dir_down = False

                rail[row][col] = '*'
                col += 1

                if dir_down:
                        row += 1
                else:
                        row -= 1
        index = 0
        for i in range(key):
                for j in range(len(cipher)):
                        if ((rail[i][j] == '*') and
                        (index < len(cipher))):
                                rail[i][j] = cipher[index]
                                index += 1
        result = []
        row, col = 0, 0
        for i in range(len(cipher)):
                if row == 0:
                        dir_down = True
                if row == key-1:
                        dir_down = False

                if (rail[row][col] != '*'):
                        result.append(rail[row][col])
                        col += 1
                if dir_down:
                        row += 1
                else:
                        row -= 1
        return("".join(result))
def check_valid(text) :
    count = 0
    for x in text.split() :
        for y in words :
            if x.lower() == y.lower() : count += 1

    if count >= 2 :
        return True

    else :
        return False

def get_message(r) :
    r.recvuntil('[i]')
    tmp = r.recvline().decode('utf-8')
   #  import pdb
   #  pdb.set_trace()
    tmp = tmp.split('=')[-1].replace("'", '')
    tmp = tmp.split()
    if tmp[0] == ' ' and tmp[-1] == ' ' :
        return ' '.join(tmp[1 : -1])
    else : 
        return ' '.join(tmp)
def main() :
    r.recvuntil(b"[?]" )
    tmp = r.recvuntil(b'= ?', drop=True).decode()
    tmp = tmp.split()

    a = ord(tmp[0])- 48
    b = ord(tmp[2]) - 48
    
    r.sendline(str(a + b).encode())
    r.send(b"Classical crypto is super easy!\n")

    ########## Round_1 #########
    msg = get_message(r)
    decode = decode_ceaser(msg)
    if check_valid(decode) :
        tmp = ' '.join([x.replace('"', '').replace('\n', '') for x in decode.split()])
        print(f"\n\n### Round 1 : ###\nplain_text : {tmp}\n")
        r.recvuntil(b'?\n')
        r.sendline(tmp.encode())
    else :
        return

    ######## Round_2 ###########
    msg = get_message(r)
    flag = True
    for i in range(2, 100) :
        decode = decode_fence(msg, i)
        if check_valid(decode) :
            flag = False
            print(f"\n\n### Round 2 : ###\nplain_text : {' '.join(decode.split())}\n")
            r.recvuntil(b'?\n')
            r.sendline((' '.join(decode.split())).encode())
            break
    if flag :
        print("####### Round 2 decode fail, not enough keywords ########\n")
        print(f"decode_message : {decode}")
        return
   
    ######## Round_3 ###########
    r.recvuntil(b"(c1) = b'")
    c1 = r.recvuntil(b"'", drop=True)
    tmp_1 = c1.decode()
    
    p1 = r.recvuntil(b"m1 = '")
    p1 = r.recvuntil(b"'", drop=True).decode()
   
    r.recvuntil(b"(c2) = b'")
    c2 = r.recvuntil(b"'", drop=True)
    tmp_2 = c2.decode()
    
    if len(tmp_1) >= len(tmp_2) :
        decode = round_3(c1, p1, c2)
    else :
        return
    if check_valid(decode) :
        print(f"\n\n### Round_3 ###\nplain_text : {decode}\n")
        r.recvuntil(b'?\n')
        r.sendline(decode.encode())
        print("\n\nFinish Round 1, 2 and 3!!\n")
        get_flag = True
        # r.interactive()
    else :
        return
    r.recvuntil(b'[i] c = ')    
    #######  Round_4 ##########
    c = r.recvline().decode().replace("'", '')
    
    tmp = r4_sent_to_binary(c) 

    # print(tmp, len(tmp))
    tmp = decrypt(tmp)
    # print(tmp)

    for i in range(2, 50) :
        print(f"i = {i}, plain_text =  {decode_fence(tmp, i)}")
    
    r.interactive()

if __name__ == "__main__" :
    times = 1
    while True :
        print(f"try {times} times.")

        # r = remote('cns.csie.org', 44398)
        r = start()
        main()
        # time.sleep(0.3)
        times += 1
        if get_flag : break
