tmp = []

with open('used.txt') as fp :
    for line in fp.read().split():
        tmp.append(line)

for i in range(len(tmp)) :
    a = tmp[i]
    for j in range(len(tmp)) :
        if i != j :
            if tmp[i] == tmp[j] :
                print(i, j)
            assert(tmp[i] != tmp[j])
