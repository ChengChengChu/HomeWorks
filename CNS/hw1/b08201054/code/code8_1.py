from pwn import *
from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes
# from cryptoFunc import *
flag1 = b'CNS{Aka_BIT_f1ipp1N9_atTaCk!}'
JOB_TITLE = 'Grand Disciplinary Officer'
NAME = 'Azar'


def recv_to_send_guess(p) :
    p.recvuntil(b'choice: ')
    p.sendline('1'.encode())
    p.recvuntil(b'(hex encoded): ')
    
    return

def decrypt_block(c, idx, p, _plain=None) :
    prev, X = [x for x in c[idx - 1]], [0 for x in range(16)]
    
    for offset in range(1, 17) :
        # print(offset)
        guess_right, is_plain = False, False
        plain_tag = 0
        # print(X)
        for guess in range(256) :
            # if offset == 2 : 
                # print(f"prev : {prev}")
                # p.interactive()
            # if offset == 2 : print(X[16 - 1], prev[16 -1])
            # if _plain is not None : print(guess)
            prev[16 - offset] = long_to_bytes(guess)
            guess_string = ''
            for i in range(len(c)) :
                if i > idx : break
                if i == (idx - 1) :
                    for j in range(16) :
                        tmp = bytes_to_long(prev[j])
                        tmp = f"0x{tmp:02x}"
                        guess_string += tmp.replace("0x", '')
                else :
                    for j in range(16) :
                        tmp = bytes_to_long(c[i][j])
                        tmp = f"0x{tmp:02x}"
                        guess_string += tmp.replace('0x', '')
            # if _plain is not None : print(guess_string)
            # if _plain is not None : p.interactive()
            recv_to_send_guess(p)
            p.sendline(guess_string.encode())
            # if _plain is not None : p.interactive()
            msg = p.recvuntil(b'\n', drop=True).decode()
            # if _plain is not None : print(msg)
            # if _plain is not None : print(f"msg : {msg}, ({long_to_bytes(guess)}, {c[idx-1][16-offset]}), {guess ^ bytes_to_long(prev[15])}")
            #### if not plain text and not padding error ####
            if "PADDING ERROR" not in msg and long_to_bytes(guess) != c[idx-1][16-offset] :
                guess_right = True
                X[16-offset] = guess ^ offset
                a = guess ^ offset 
                flag = False
                for j in range(16-offset, 16) :
                    prev[j] = long_to_bytes((offset + 1) ^ X[j])
                
                if offset == False :
                    # print("DEBUG\n")
                    my_plain = bytearray(b'')
                    for j in range(16 - offset, 16) : 
                        b = X[j] ^ bytes_to_long(c[idx-1][j])
                        my_plain.append(b)
                    
                    print(f"my decode : {my_plain}")
                    check_next = bytearray(b"")
                    for j in range(16 - offset, 16) :
                        b = bytes_to_long(prev[j]) ^ X[j]
                        check_next.append(b)
                    print(f"check next itr padding correct : {check_next}")

                    print(guess, offset, '\n') 
                    print(f"prev : {prev}, X : {X}")
                    print(X[16-offset] ^ bytes_to_long(prev[16-offset]))
                    # p.interactive()
                    print(f"aaa prev : {prev}")
                    # p.interactive()
                break

            elif "PADDING ERROR" not in msg : 
                is_plain = True
                plain_tag = guess
        if not guess_right and is_plain : 
            X[16 - offset] = plain_tag ^ offset
            a = plain_tag ^ offset 
            
            for j in range(16 - offset, 16) : 
                prev[j] = long_to_bytes((offset + 1) ^ X[j])
            
            my_plain = bytearray(b'')
            for j in range(16 - offset, 16) :
                b = X[j] ^ bytes_to_long(c[idx-1][j])
                my_plain.append(b)
            
            # print(f"my decode : {my_plain}")
            check_next = bytearray(b"")
            for j in range(16 - offset, 16) :
                b = bytes_to_long(prev[j]) ^ X[j]
                check_next.append(b)
            # print(f"check next itr padding correct : {check_next}")
        
    ##### get plain text ######
    plain_text = ""
    pad_len = 0
    if idx == len(c) - 1 : pad_len = X[-1] ^ bytes_to_long(c[idx-1][-1])
    for i in range(0, 16- pad_len) :
        tmp = X[i] ^ bytes_to_long(c[idx - 1][i])
        tmp = long_to_bytes(tmp)
        # print(tmp, '\n\n\n')
        if _plain is None:
            plain_text += tmp.decode()
    
    # print("PASS")
    if _plain is not None :
        assert(len(X) == len(_plain[idx]))
        tmp = [x ^ y for x, y in zip(X, _plain[idx])] 
        # print(f"Before modify, c : {c[idx-1]} " )
        for i in range(16) :
            c[idx-1][i] = long_to_bytes(tmp[i])
        # print(f"After modify, c : {c[idx-1]}")


    # print(plain_text, '\n\n\n')
    return plain_text, X 

def main() :
    info = f'job title:{JOB_TITLE}||name:{NAME}||secret word:{flag1.decode()}'.encode()
    # p = remote('cns.csie.org', 44399)
    p = process(['python3', 'server.py'])
    p.recvuntil(b'ID: ')
    ID = p.recvuntil(b'----+', drop=True).decode().replace('\n', '').replace('-', '').replace('+', '').replace('|', '').replace(' ', '')
    ####### set mode to get oracle ##########
    p.recvuntil(b'our choice: ')
    p.sendline('2'.encode())
    ####### construct hex blocks ############
    print(ID, len(ID))
    # p.interactive()    
    tmp = bytes.fromhex(ID)
    # print(tmp, len(tmp))
    c, t = [], []
    idx = 0
    while idx < len(tmp) :
        t.append(long_to_bytes(tmp[idx]))
        if len(t) == 16 : 
            c.append(t)
            t = []
        
        idx += 1
    # print(c)
    idx = len(c) - 1
    tmp = []
    X = []
    # my_cipher = copy.deepcopy(c)
    while idx >= 1  :
        print(idx)
        #### flag1 #####
        x, _ = decrypt_block(c, idx, p)
        tmp.append(x)
        
        with open('flag1_result_2.txt', 'a') as fp :
            fp.write(str(idx) + ' ')
            for i in range(len(_)) :
               fp.write(str(_[i]) + ' ') 
        #### flag2 #####
        X.append(_)
        idx -= 1
    
    with open ('dec.txt', 'w') as fp :
        for i in range(len(X)) :
            fp.write(f"{i} ")
            for j in range(len(X[i])) :
                fp.write(str(X[i][j]) + ' ')
            fp.write('\n')
    print("\n[INFO] : Decrypying flag1\n")
    # print(f"tmp : {tmp}")
    tmp.reverse()
    plain = ''.join([x for x in tmp])
    p.recvuntil(b'Your choice: ')
    p.sendline('3'.encode())
    # print(plain)
    # print(f"word : {plain}")
    word = plain.split(":")[-1]
    p.recvuntil(b'choice: ')
    p.sendline('1'.encode())
    p.recvuntil(b"word: ")
    p.sendline(word.encode())
    
    ########## for flag 2
    print(f"flag1 : {word}\n")
    #p.interactive()
    p.recvuntil(b'choice: ')
    p.sendline('2'.encode())
    # p.interactive()
    #### calculate #####
    idx = 0
    my_plain, tmp = [], []
    print(f"my info : {info}") 
    length = 16 - len(info) % 16 
    info += chr(length).encode()*length

    while idx < len(info) :
        tmp.append(info[idx])
        if len(tmp) % 16 == 0 :
            my_plain.append(tmp)
            tmp = []
        idx += 1
    
    for i in range(len(my_plain)) :
        print(f"block {i}")
        for j in range(len(my_plain[i])) :
            print(f"{j} {long_to_bytes(my_plain[i][j]).decode()}")
        print('=' * 10)
    
    idx = len(c) - 1
    while idx >= 100000 :
        print(idx)
        decrypt_block(c, idx, p, my_plain)
        idx -= 1

    X.reverse()    
    ### calculate block 2 ###
    block_1 = [0 for i in range(16)]
    
    for i in range(16) :
        block_1[i] = X[1][i] ^ my_plain[2][i]
    
    my_cipher = ""
    
    for i in range(16) :
        tmp = block_1[i]
        tmp = f"0x{tmp:02x}"
        my_cipher += tmp.replace('0x', '')

    print(my_cipher)
    
    print('\n\n')
    print(ID, '\n')

    my_cipher_ = ""
    for i in range(32) :
        my_cipher_ += ID[i]
    for i in range(32) :
        my_cipher_ += my_cipher[i]

    for i in range(64, len(ID)) :
        my_cipher_ += ID[i]
    
    print(my_cipher_)
    _ = 0

    print(ID)
    
    print("=================")
    print(X)
    print("=" * 100)
    print(c)

    print('=' * 100)
    print(my_plain)
    p.interactive()
    for i in range(0) :
        my_cipher += ID[i]
    

    for i in range(len(c)) :
        for j in range(len(c[i])) :
            tmp = bytes_to_long(c[i][j])
            tmp = f"0x{tmp:02x}"
            my_cipher += tmp.replace("0x", '')

    print(my_cipher)
    #for i in range(len(t)) :
    #    tmp = t[i]
    #    tmp = f"0x{tmp:02x}"
    #    tmp = tmp.replace("0x", '')
    #    my_cipher += tmp

    # offset = 32
    # while offset >= 1 :
    #     my_cipher += ID[len(ID) - offset]
    #    offset -= 1

    #print(my_cipher)
    #print(len(my_plain))
    p.interactive()
    #print(plain)



if __name__ == '__main__' :
    main()
