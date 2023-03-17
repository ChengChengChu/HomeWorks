import base64
def round_3(cypher_1, plain_1, cypher_2) : 
    # print(type(cypher_1), type(plain_1), type(cypher_2))
    tmp = bytes(c ^ p for c, p in zip(base64.b64decode(cypher_1), base64.b64decode(cypher_2)))


    plain_1 = plain_1.encode()
    plain_2 = bytes(c ^ p for c, p in zip(tmp, plain_1))
    return plain_2.decode()
def sent_to_upper(s) :
    tmp = [x.upper() for x in s.split()]

    return " ".join(tmp)

