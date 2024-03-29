from pwn import *
# from server import *

get_flag = 3

def main() :
    # p = process(['python', 'server.py'])
    p = remote('cns.csie.org', 44377)
    with open("shattered-1.pdf", "rb") as pdf_file:
        encoded_string_1 = pdf_file.read()

    with open("shattered-2.pdf", "rb") as pdf_file:
        encoded_string_2 = pdf_file.read()
    
    encoded_string_1 += b"I love CNS"
    encoded_string_2 += b"I love CNS"

    ###### register user_1 
    p.recvuntil(b'Your choice: ')
    p.sendline(str(1).encode())
    
    p.recvuntil(b'Username: ')
    p.sendline(encoded_string_1)
    p.recvuntil(b'place: ')

    pass_word_1 = p.recvuntil(b'\n', drop=True).decode()
    
    ##### register user_2
    p.recvuntil(b'Your choice: ')
    p.sendline(str(1).encode())
    
    p.recvuntil(b'Username: ')
    
    p.sendline(encoded_string_2)
    p.recvuntil(b'place: ')

    pass_word_2 = p.recvuntil(b'\n').decode()
    
    #### buy flag1
    p.recvuntil(b'Your choice: ')
    p.sendline(str(2).encode())
    
    p.recvuntil(b'Username: ')
    p.sendline(encoded_string_1)
    p.recvuntil(b'Base64: ')
    p.sendline(pass_word_1.encode())
    # p.interactive()
    p.recvuntil(b'Your choice: ')
    # p.interactive()
    p.sendline(str(get_flag).encode())
    
    to_recv = str((get_flag - 1)) + ':'
    p.recvuntil(to_recv.encode())
    flag = p.recvuntil(b'\n', drop=True).decode()
    print(f'flag {get_flag-1} : {flag}')

    # p.interactive()


if __name__ == '__main__' :
    main()
