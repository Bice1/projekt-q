a = 8

All_modr3 = []
for i in range(a-1):
    All_modr3.append([])
    for j in range(a-1):
        All_modr3[i].append([])
for i in range(a-1):
    for j in range(i+1,a-1,1):
        All_modr3[i][j]=[4, 2, 3]
        All_modr3[j][i]=[4, 2, 3]
print(All_modr3)
for i in range(a-1):
    print(All_modr3[i])
    print(All_modr3[i][:][:][:][2])
    All_modra1 = []
    All_modra2 = []
    All_modra3 = []
    for idx,k in enumerate(All_modr3[i]):
        if idx == i:
            continue
        All_modra1.append(k[0])
        All_modra2.append(k[1])
        All_modra3.append(k[2])
    print(All_modra1,All_modra2,All_modra3)