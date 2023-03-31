from pwn import *
from sympy.ntheory import discrete_log
from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes

def main() :
    # p = process(['python', 'stage3.py'])
    p = remote('cns.csie.org', 6003)
    p.recvuntil(b"P = ")
    P = int(p.recvuntil(b'\n', drop=True).decode())
    _p = (P - 1) // 2 
    p.recvuntil(b'g = ')
    g = int(p.recvuntil(b'\n', drop=True).decode())
    p.recvuntil(b'cipher = (')
    
    gy = int(p.recvuntil(b', ', drop=True).decode())
    cypher_text = int(p.recvuntil(b')', drop=True).decode())
    points = {}
    for i in range(1, 6) :
        # print("PASS")
        p.recvuntil(b'(y/n):')
        p.sendline('y'.encode())
        tmp = str(gy)# str(bytes_to_long('A'.encode()))
        p.recvuntil('your c1:'.encode())
        p.sendline(tmp.encode())
        # p.interactive()
        p.recvuntil('(1~5):'.encode())
        p.sendline(str(i).encode())
        
        tmp = int(p.recvuntil(b'\n').decode())
        points[i] = tmp
    
    ### calculate lagrange polynomial
    result = 1
    for i in range(1, 6) :      
        up, down = 1, 1
        for j in range(1, 6) :
            if i == j : continue
            else :
                up = up * (0 - j) % _p
                down = (down * (i - j)) % _p
         
        down = pow(down, -1, _p)
        l_i = (up * down) % _p

        result = (result * pow(points[i], l_i, P)) % P
    
    my_key = pow(result, -1, P)
    d = (my_key * cypher_text) % P
    print(long_to_bytes(d).decode())
    # print(long_to_bytes(d).decode())

if __name__ == '__main__' :
    main()
