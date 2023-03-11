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

r = remote('cns.csie.org', 44398)
# r.interactive()
r.recvuntil("[?]" )

tmp = r.recv()
tmp = tmp.decode('utf-8')
# print(tmp)
tmp = tmp.split()
# print(tmp)
a = ord(tmp[0])- 48
b = ord(tmp[2]) - 48
#print(a, b)
#print(str(a + b))
r.send(str(a + b) + '\n')
r.send("Classical crypto is super easy!\n")
# while True : 
r.recvuntil('[i]')
tmp = r.recvline().decode('utf-8')
# print(tmp,'\n' +  '=' * 100)
tmp = tmp.split('=')[-1].replace("'", '')

##### decode ########
# print(decode_ceaser(tmp), '\n\n\n\n')
a = decode_ceaser(tmp)
# print(type(a))
decode = ' '.join(a.split())
# print('===', a.split(), '===')
print("decode message : ", decode)
r.sendline(decode)

r.interactive()
r.recvuntil('[i]')
tmp = r.recvline().decode('utf-8')

tmp = tmp.split('=')[-1].replace("'", '')
# print('\n\n', tmp, '\n\n')

print(decode_ceaser(tmp))
r.interactive()


