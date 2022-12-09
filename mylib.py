from ctypes import *
import sys
""""
if str(sys.platform) == "linux":
    lib_path = f'./mylib_{sys.platform}.so'
else :
    lib_path = f'./mylib_{sys.platform}.dll'
"""
lib_path = f'C:/Users/quent/OneDrive/Desktop/projet_fin/mylib.so'
clib = CDLL("C:/Users/quent/OneDrive/Desktop/projet_fin/mylib.so")
c_g_force = clib.c_g_force
c_g_force.restype = None 

def func_c_g_force(gravconst_mata,All_r_interaction_lisa,All_modr3a, indexplanet):
    n = len(gravconst_mata)
    gravconst_mata_in = (c_double * n)(*gravconst_mata)
    All_r_interaction_lisa_in = (c_double * n-1)(*All_r_interaction_lisa)
    All_modr3a_in= (c_double * n)(*All_modr3a)
    f_out = (c_double * n-1)
    c_g_force(gravconst_mata_in, All_r_interaction_lisa_in,All_modr3a_in,c_int(indexplanet),c_int(n), f_out)
    return f_out