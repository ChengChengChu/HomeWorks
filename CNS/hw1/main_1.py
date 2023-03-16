from pwn import *
import time 
import random
import base64
import warnings  
warnings.filterwarnings("ignore")  


words = []
get_flag = False
with open('common_words.txt', 'r') as fp :
    for line in fp.read().splitlines() :
        words.append(line)

def round_3(cypher_1, plain_1, cypher_2) :

    # print(base64.b64decode(cypher_1))
    # print(plain_1.encode('utf-8'))
    tmp = bytes(c ^ p for c, p in zip(base64.b64decode(cypher_1), base64.b64decode(cypher_2)))

    # print(f"\n### cypher_1 xor cypher_2 == {tmp} ###\n")

    plain_2 = bytes(c ^ p for c, p in zip(tmp, plain_1.encode())).decode()

    return plain_2


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

def round_3(cypher_1, plain_1, cypher_2) :
    # print(type(cypher_1), type(plain_1), type(cypher_2))
    # print(cypher_1, plain_1, cypher_2)
    # print(base64.b64decode(cypher_1))
    # print(plain_1.encode('utf-8'))
    tmp = bytes(c ^ p for c, p in zip(base64.b64decode(cypher_1), base64.b64decode(cypher_2)))

    # print(f"\n### cypher_1 xor cypher_2 == {tmp} ###\n")

    plain_2 = bytes(c ^ p for c, p in zip(tmp, plain_1.encode())).decode()

    return plain_2


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
    # print("pass\n")
    # r = remote('cns.csie.org', 44398)
   #  r.interactive()
    r.recvuntil("[?]" )

    tmp = r.recv()
    tmp = tmp.decode('utf-8')
    tmp = tmp.split()

    a = ord(tmp[0])- 48
    b = ord(tmp[2]) - 48
    
    r.send(str(a + b) + '\n')
    r.send("Classical crypto is super easy!\n")

    ########## Round_1 #########
    msg = get_message(r)
    decode = decode_ceaser(msg)
    if check_valid(decode) :
        #print(f"\n\n#### Round 1 : ####\nplain_text : {' '.join(decode.split())}\n")
        tmp = ' '.join([x.replace('"', '').replace('\n', '') for x in decode.split()])

        print(f"\n\n### Round 1 : ###\nplain_text : {tmp}\n")
        r.sendline(tmp)
    else :
        # print("####### Round 0 : not enough keywords ##########")
        # print(f"decodec_message : {decode}")
        # exit(0)
        return

    ######## Round_2 ###########
    msg = get_message(r)
    flag = True
    # print(f"cypher text : {msg}\n")
    for i in range(2, 100) :
        decode = decode_fence(msg, i)
        if check_valid(decode) :
            flag = False
            print(f"\n\n### Round 2 : ###\nplain_text : {' '.join(decode.split())}\n")
            r.sendline(' '.join(decode.split()))
            break
            #print(check_valid(decode), decode)
        #else :
        #    print("Not plain_text")
    if flag :
        # print("####### Round 2 decode fail, not enough keywords ########\n")
        # print(f"decode_message : {decode}")
        # exit(1)
        return
    get_flag = True
    # r.interactive()
    r.recvline()
    
    r.recvline()
    r.recvline()
    
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvuntil('= ')
    c_1 = r.recvline().decode().replace('\n', '').replace('b', '').replace("'", '')# .encode()
    # print(f"c_1 : {c_1}")
    # r.interactive() 
    r.recvuntil('= ')
    p_1 = r.recvline().decode().replace('\n', '').replace('"', '').replace("'", '')
    # print(f"p_1 : {p_1}\n\n")
    
    r.recvuntil('= ')
    c_2 = r.recvline().decode().replace('\n', '').replace('b', '').replace("'", '')#.encode()
    # print(f"c_2 : {c_2}")
    # s + b'=' * (-len(s) % 4) 
    # r.interactive()
    # msg = r.recvline().decode().replace('\n', '').replace('b', '').replace("'", '').encode()
    # print(len(c_1), len(c_2))
    # r.interactive()
    if len(c_1) >= len(c_2) :
        decode = round_3(c_1.encode(), p_1, c_2.encode())
    else:
        return
    # print(type(msg.encode()), msg.encode(), 'fuck\n\n')
    # msg = msg.split()[-1].replace('"', '').replace('b', '').replace("'", '')    
    
    # print(len(msg), '\n\n\n\n\n')
    # import pdb
    # pdb.set_trace() 
    if check_valid(decode) :
        print(f"### Round_3 plain_text : {decode} ###")
        r.sendline(decode)
        print("Finish Round 1, and 2 !!\n")
        # r.interactive()
    else :
        return
    
    r.recvuntil('Hint2: You can safely ignore all white spaces and punctuation marks.')
    # r.interactive()
    r.recvline()
    r.recvline()
    r.recvuntil('= ')
    msg = r.recvline().decode().replace('\n', '').replace("'", '')
    # print('\n\n', msg, '\n\n')
    msg = ' '.join([x.upper() for x in msg.split()])
    print('\n\n\n', msg, '\n\n\n')
    r.sendline(msg)
    # r.interactive()


if __name__ == "__main__" :
    times = 1
    while True :
        print(f"try {times} times.")

        r = remote('cns.csie.org', 44398)
        main()
        # time.sleep(0.3)
        times += 1
        if get_flag : break
