from itertools import permutations

words = []
with open('common_words.txt', 'r') as fp :
    for line in fp.read().splitlines() :
        words.append(line)

def decode_ceaser(text, max_len) :
    for offset in range(max_len) :
        decode = ""
        for x in text :
            if ord(x) >= 97 and ord(x) <= 122 :
                decode += chr((ord(x) + offset - 97) % max_len + 97)
            elif ord(x) >= 65 and ord(x) <= 90 :
                decode += chr((ord(x) + offset - 65) % max_len + 65)
            else :
                decode += x
        count = 0
        for d in decode.split() :
            for w in words :
                if d == w :
                   #  print(d)
                    count += 1
        if True :
            # print("========\n", decode, "========\n")
            print(f"offset : {offset}, text : {decode}")
            continue

    return "Not enough common_words"
text = []
with open("encoded.txt", 'r') as fp :
    for line in fp.read().splitlines() :
        text.append(line)

_ = text[0].replace("'", "")
# _ = "yod"

# perms = [''.join(p) for p in permutations(_)]

# _ = "yod"
# print(perms)
decode_ceaser(_, 26)


