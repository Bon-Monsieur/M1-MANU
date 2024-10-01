#%%

import numpy as np

#%%

a = 1
up_a = np.cos(1)


def u(x):
    return np.sin(x)

def Dp_u(x,h):
    return (u(x+h)-u(x))/h

def Dm_u(x,h):
    return (u(x)-u(x-h))/h

def D0_u(x,h):
    return (u(x+h)-u(x-h))/(2*h)

def D3_u(x,h):
    return (2*u(x+h)+3*u(x)-6*u(x-h)+u(x-2*h))/(6*h)

h = [1e-1, 5e-2, 1e-2, 5e-3, 1e-3] 

T_Dp = [Dp_u(a,t) for t in h]
T_Dm = [Dm_u(a,t) for t in h]
T_D0 = [D0_u(a,t) for t in h]
T_D3 = [D3_u(a,t) for t in h]
print(T_Dp)
print(T_Dm)
print(T_D0)
print(T_D3)



#%%