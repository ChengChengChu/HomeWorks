import base64

lookup = {'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
          'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
          'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
          'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
          'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa', 'Z': 'bbaab'}
 

def round_3(cypher_1, plain_1, cypher_2) : 
    # print(type(cypher_1), type(plain_1), type(cypher_2))
    tmp = bytes(c ^ p for c, p in zip(base64.b64decode(cypher_1), base64.b64decode(cypher_2)))


    plain_1 = plain_1.encode()
    plain_2 = bytes(c ^ p for c, p in zip(tmp, plain_1))
    return plain_2.decode()

def r4_sent_to_binary(s) :
    # tmp = [x.upper() for x in s.split()]
    # 65 ~ 90 : upper
    # 97 ~ 122 : lower
    ret = ''
    for x in s :
        k = ord(x)
        # print(type(k))
        if k >= 65 and k <= 90 :
            ret += 'b'
        elif k >= 97 and k <= 122 :
            ret += 'a'
        # else :
            # print(x, '==')
    return ret

def decrypt(message):
    decipher = ''
    i = 0
 
    # emulating a do-while loop
    while True:
        # condition to run decryption till
        # the last set of ciphertext
        if(i < len(message)-4):
            # extracting a set of ciphertext
            # from the message
            substr = message[i:i + 5]
            # checking for space as the first
            # character of the substring
            if(substr[0] != ' '):
                '''
                This statement gets us the key(plaintext) using the values(ciphertext)
                Just the reverse of what we were doing in encrypt function
                '''
                decipher += list(lookup.keys()
                                 )[list(lookup.values()).index(substr)]
                i += 5  # to get the next set of ciphertext
 
            else:
                # adds space
                decipher += ' '
                i += 1  # index next to the space
        else:
            break  # emulating a do-while loop
 
    return decipher
 


