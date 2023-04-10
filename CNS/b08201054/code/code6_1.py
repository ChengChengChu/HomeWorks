from pwn import *
from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes

def main() :
    # p = process(['python', 'stage1.py'])
    p = remote('cns.csie.org', 6001)
    #### get P and g
    p.recvuntil(b'P = ')
    P = int(p.recvuntil(b'\n', drop=True).decode())
    p.recvuntil(b'g = ')
    g = int(p.recvuntil(b'\n', drop=True).decode())
    
    #### get key and encoded flag
    p.recvuntil(b'cipher = (')
    K1 = int(p.recvuntil(b', ', drop=True).decode())
    encoded_flag = int(p.recvuntil(b')\n', drop=True))
    p.recvuntil(b'(y/n):')
    p.sendline(b'y')
    p.recvuntil(b'Give me your message:')
     
    
    for i in range(97, 256) :
        A = long_to_bytes(i).decode()
        if pow(i, 2, P) != 1 and pow(i, (P-1)//2, P) != 1: 
            break
    
    # print(f"send : {A}\n\n")
    p.sendline(str(A).encode())
    
    ### get cypher text ### 
    p.recvuntil(b', ', drop=True)
    my_cypher = int(p.recvuntil(b')\n', drop=True).decode())
    
    inv = bytes_to_long(A.encode())
    inv = pow(inv, -1, P)
    my_key = (my_cypher * inv) % P
    # print(f'\n\nmy_key : {my_key}\n\n')
    # p.interactive()
    my_key = pow(my_key, -1, P)

    
    # print(f'\n\nmy_key : {my_key}\n\n')
    decrypt = (my_key * encoded_flag) % P
    print(long_to_bytes(decrypt).decode())
    
if __name__ == '__main__'  :
    main()
