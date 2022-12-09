import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import animation
import csv
import sys
import os
import ctypes
from mylib import func_c_g_force
#os.system('/main.exe qg& qrgé')
def readfile(name):
    file = open(name)
    csvReader = csv.reader(file,delimiter=';')
    return csvReader
G           = 6.67e-11
AU          = 1.5e11

filename1 = "main.csv"
temp = 0
templist = []
for line in readfile(filename1):
    if temp ==0:
        temp += 1
        continue
    templist.append(line[0])
    print(f"{temp} - {line[1]}")
    temp += 1
while True :
    x = 4#input("Which system do you want to visualize ?")
    try :
        if 1 <= int(x) <= temp:
            break
        print('An Error occured')
        if input('Would you want to stop ? if yes, please write "Yes" ') == "Yes":
            x = None
            break
        continue
    except :
        print('An Error occured')
        if input('Would you want to stop ? if yes, please write "Yes" ') == "Yes":
            x = None
            break
        continue
if x == None:
    sys.exit()
temp = 0
for line in readfile("Configuration/"+templist[x-1]):
    if temp ==0:
        temp += 1
        continue
    filename = line[0]
    dtincr = float(line[1])
    tsimu = int(line[2])
    axis_size = float(line[3])
    description = line[4]

a = 0
MassList = []
ap_v_y = []
ap_v_z = []
orbit_diameter_ap = []
color = []
name = []
markersize = []
for line in readfile("data/"+filename):
    
    if a ==0:
        a += 1
        continue
    MassList.append(float(line[1]))
    ap_v_y.append(float(line[4]))
    orbit_diameter_ap.append(float(line[3])*AU)
    ap_v_z.append(float(line[5]))
    color.append(line[6])
    name.append(line[0])
    markersize.append(int(line[2]))
    a += 1
daysec      = 24.0*60*60

Gravconst_mat = []
for i in range(a-1):
    Gravconst_mat.append([])
    for j in range(a-1):
        Gravconst_mat[i].append([])
for i in range(a-1):
    for j in range(a-1):
        if i == j:
            continue
        Gravconst_mat[i][j] = MassList[i]*MassList[j]*G

All_x = []
All_y = []
All_z = []
All_vx = []
All_vy = []
All_vz = []
for i in range(a-1):
    All_x.append(orbit_diameter_ap[i])
    All_y.append(0)
    All_z.append(0)
    All_vx.append(0)
    All_vy.append(ap_v_y[i])
    All_vz.append(ap_v_z[i])
All_save_x = []
All_save_y = []
All_save_z = []
for i in range(a-1):
    All_save_x.append([All_x[i]])
    All_save_y.append([All_y[i]])
    All_save_z.append([All_z[i]])

t           = 0.0
dt          = dtincr*daysec

def Compute_force_G_on_a(gravconst_mata,All_r_interaction_lisa,All_modr3a, indexplanet):
    fx_a_x = []
    idx = 0
    for i in range(a-1):
        if i == indexplanet:
            continue
        fx_a_x.append(gravconst_mata[i]*All_r_interaction_lisa[idx]/All_modr3a[i]) 
        idx += 1
        #à faire en c
    return fx_a_x

    
All_r_interaction_list = []
for i in range(a-1):
    All_r_interaction_list.append([])
    for j in range(a-1):
        All_r_interaction_list[i].append([])

All_modr3 = []
for i in range(a-1):
    All_modr3.append([])
    for j in range(a-1):
        All_modr3[i].append([])

#monC = ctypes.CDLL("C:\Users\projet_fin\main.dll")
#end = monC.simu(dtincr,tsimu,a,ctypes.c_char_p("data/"+filename))

while t<tsimu*365*daysec:
    for i in range(a-1):
        for j in range(i+1,a-1,1):
            [rx, ry, rz] = [All_x[j]-All_x[i],All_y[j]-All_y[i],All_z[j]-All_z[i]]  #à faire en c
            All_r_interaction_list[i][j]=[rx, ry, rz]  
            All_r_interaction_list[j][i]=[-rx, -ry, -rz]         
            All_modr3[i][j]=(rx**2+ry**2+rz**2)**1.5
            All_modr3[j][i]=All_modr3[i][j]
    for i in range(a-1):
        All_interactiona1 = []
        All_interactiona2 = []
        All_interactiona3 = []
        for idx,k in enumerate(All_r_interaction_list[i]):
            if idx == i:
                continue
            All_interactiona1.append(k[0])
            All_interactiona2.append(k[1])
            All_interactiona3.append(k[2])
        fx = func_c_g_force(Gravconst_mat[i],All_interactiona1,All_modr3[i], i)
        fy = func_c_g_force(Gravconst_mat[i],All_interactiona2,All_modr3[i], i)
        fz = func_c_g_force(Gravconst_mat[i],All_interactiona3,All_modr3[i], i)
        All_vx[i] += np.sum(fx)*dt/MassList[i]   #a faire en c
        All_vy[i] += np.sum(fy)*dt/MassList[i]
        All_vz[i] += np.sum(fz)*dt/MassList[i]

        All_x[i]+=All_vx[i]*dt #a faire en c
        All_y[i]+=All_vy[i]*dt
        All_z[i]+=All_vz[i]*dt

        All_save_x[i].append(All_x[i])
        All_save_y[i].append(All_y[i])
        All_save_z[i].append(All_z[i])
            
    t += dt


print('data ready')

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import animation

fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')
ax.axis('auto')


ax.set_xlim(-axis_size*AU,axis_size*AU)
ax.set_ylim(-axis_size*AU,axis_size*AU)
ax.set_zlim(-axis_size*AU,axis_size*AU)

# ax.set_aspect('auto')
# ax.grid()
datadict = {}
vis_dict = {}
line= []
point= []
text = []
dataset = []
for i in range(a-1):
    line.append(1)
    point.append(1)
    text.append(1)
    dataset.append(1)

for i in range(a-1):
    line[i], = ax.plot([0],[0],[0],'-',color = color[i], lw=1)
    point[i], = ax.plot([orbit_diameter_ap[i]],[0],[0], marker="o", markersize=markersize[i], markeredgecolor=color[i], markerfacecolor=color[i])
    text[i]= ax.text(orbit_diameter_ap[i],0,0,name[i])
    vis_dict[i] = [line[i],point[i],text[i]]
    datadict[i] = [All_save_x[i],All_save_y[i],All_save_z[i]]
    dataset[i] = datadict[i]
def update(num,datadict,vis_dict):
    for i in range(a-1):
        dataset[i] = datadict[i]
        line[i],point[i],text[i]   = vis_dict[i][0],vis_dict[i][1],vis_dict[i][2]
        line[i].set_data_3d(dataset[i][0][:num],dataset[i][1][:num], dataset[i][2][:num])
        point[i].set_data_3d(dataset[i][0][num],dataset[i][1][num], dataset[i][2][num])
        text[i].set_position((dataset[i][0][num],dataset[i][1][num],dataset[i][2][num]))

ani = animation.FuncAnimation(
    fig
    ,update
    ,len(All_save_x[0])
    ,fargs=(datadict, vis_dict)
    ,interval=1
)

plt.title(description)
plt.show()