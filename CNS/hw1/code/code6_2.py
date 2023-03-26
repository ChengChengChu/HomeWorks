from pwn import *
from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes

def main() :
    # p = process(['python', 'stage2.py'])
    p = remote('cns.csie.org', 6002)
    p.recvuntil(b'P = ')
    
    P = int(p.recvuntil(b'\n', drop=True).decode())
    
    p.recvuntil(b'g = ')
    g = int(p.recvuntil(b'\n', drop=True).decode())
    p.recvuntil(b'cipher = (')

    gy = int(p.recvuntil(b', ', drop=True).decode())

    cypher_flag = int(p.recvuntil(b')', drop=True).decode())
    

    min_flag = 'flag: CNS{'
    max_flag = 'flag: CNS{'
    for i in range(32) :
        min_flag += '!'
        max_flag += '}'

    min_flag += '}'
    max_flag += '}'
    L, R = pow(2, 1024, P) // bytes_to_long(max_flag.encode()), pow(2, 1024, P) // bytes_to_long(min_flag.encode())
    mid = 0
    while L <= R :
        mid = (L + R) // 2
        
        p.recvuntil(b'(y/n): ')
        p.sendline(b'y')

        p.recvuntil(b'c1: ')
        p.sendline(str(gy).encode())
        
        p.recvuntil(b'c2: ')
        p.sendline(str((mid * cypher_flag) % P).encode())
        
        res = p.recvuntil(b'\n').decode()

        # < 128
        if res[0] == 'O' :
            L = mid + 1
        # >= 128
        else :
            R = mid - 1
            
    x = L
    K = pow(2, 1024, P)
    l = 36716799847279585879321362750050668098891237468855127936084578418179513498101361968176439280864260305264111496466904671759510010282245352480196034250427095155505464165168217228568526693389563202408154971007166193285459655712843890719293430237345391593145225518642449604582180378073501

    guess_count = 0 
    for i in range((l - 100), P) :
        tmp1 = (K + i) * pow(x, -1, P) % P
        tmp2 = (K - i) * pow(x, -1, P) % P
        if guess_count % 10 == 0 :print(f'guess {guess_count} times')
        guess_count += 1
        if len(long_to_bytes(tmp1)) <= 50 and long_to_bytes(tmp1)[-1] == bytes_to_long(b'}') :
            print(long_to_bytes(tmp1).decode())
            break

        if len(long_to_bytes(tmp2)) <= 50 and long_to_bytes(tmp2)[-1] == bytes_to_long(b'}') :
            print(long_to_bytes(tmp2).decode())
            break


if __name__ == '__main__' :
    main()
