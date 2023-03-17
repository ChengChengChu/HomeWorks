from main_1 import *

S = 'Oh GOod! I wAS jUST THinKInG that the SiLk flOweRS at the feiyuN coMMErCe guilD nEedEd WateRinG. the tRANsPORT cOoRdiNAToRs wILl proBAblY MoaN abouT the MUddy mOUNTaiN roaDS AGAin, though...'

upper = "QWERTYUIOPLKJHGFDSAZXCVBNM"

def sent_to_upper(s) :
    #tmp = [x.upper() for x in s.split()]
    tmp = []
    for x in s :
        if x in upper :
            tmp.append(x)

    return tmp


t = sent_to_upper(S)
for i in range(2, 10) :

    tmp = decode_fence(t, i)
    print(tmp)
