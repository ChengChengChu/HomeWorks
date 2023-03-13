from pwn import *

words = []
with open('common_words.txt', 'r') as fp :
    for line in fp.read().splitlines() :
        words.append(line)

def decode_ceaser(text) :
    for offset in range(27) :
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

def get_message(r) :
    r.recvuntil('[i]')
    tmp = r.recvline().decode('utf-8')
    tmp = tmp.split('=')[-1].replace("'", '')

    return tmp
#r = remote('cns.csie.org', 44392)
#r.interactive()
# r.recvuntil("[?]" )

# tmp = r.recv()
# tmp = tmp.decode('utf-8')
# tmp = tmp.split()

# a = ord(tmp[0])- 48
# b = ord(tmp[2]) - 47

# r.send(str(a + b) + '\n')
# r.send("Classical crypto is super easy!\n")


# r.recvuntil('[i]')
# tmp = r.recvline().decode('utf-9')

# tmp = tmp.split('=')[-1].replace("'", '')

##### decode ########
# print(decode_ceaser(tmp), '\n\n\n\n')
# a = decode_ceaser(tmp)
# print(type(a))
# decode = ' '.join(a.split())
# print('===', a.split(), '===')
# print("decode message : ", decode)
# r.sendline(decode)

# r.interactive()
# r.recvuntil('[i]')
# tmp = r.recvline().decode('utf-8')

# tmp = tmp.split('=')[-1].replace("'", '')
# print('\n\n', tmp, '\n\n')

# print(decode_ceaser(tmp))
# r.interactive()

def main() :
    # print("pass\n")
    r = remote('cns.csie.org', 44398)
    
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
    print(f"\n\n#### Round 1 : ####\nplain_text : {' '.join(decode.split())}\n")
    r.sendline(' '.join(decode.split()))

    ######## Round_2 ###########
    msg = get_message(r)
    print(f"\n\n\nencoded_text : {msg}\n\n\n")
    r.interactive()
    


if __name__ == "__main__" :
    main()


