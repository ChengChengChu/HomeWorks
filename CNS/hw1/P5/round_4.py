from main_1 import *
from utils import *

c = input().replace("'", '')

tmp = r4_sent_to_binary(c) 

# print(tmp, len(tmp))
tmp = decrypt(tmp)
# print(tmp)

for i in range(2, 50) :
    print(f"i = {i}, plain_text =  {decode_fence(tmp, i)}")
