#%%
import numpy as np
import matplotlib.pyplot as plt

# QUESTION A.2
def u1(x,y):
    return np.cos(x**4+y**2)

def u2(x,y):
    return np.sin(x**4+y**2)

def u(x,y):
    return np.array([u1(x,y),u2(x,y)])



def  Lhu(x,y,h):
    return 1/(2*h)* np.array([[u1(x+h,y)-u1(x-h,y),u1(x,y+h)-u1(x,y-h)],
    [u2(x+h,y)-u2(x-h,y),u2(x,y+h)-u2(x,y-h)]])


def grad_u(x,y):
    return np.array([[-4*x**3*u2(x,y),-2*y*u2(x,y)],
    [4*x**3*u1(x,y),2*x*u1(x,y)]])

def e_h(x,y,h):
    return Lhu(x,y,h) - grad_u(x,y)


x = [1,1]
h = [1e-1, 5e-2, 1e-2, 5e-3, 1e-3]

epsh = [e_h(x[0],x[1],hi) for hi in h]


# QUESTION A.3
def L_inf(eh):
    return max([np.abs(eh[0,0])+np.abs(eh[0,1]),np.abs(eh[1,0])+np.abs(eh[1,1])])

n_inf = [L_inf(eh) for eh in epsh]

plt.loglog(h,n_inf,label='norm_inf')

# QUESTION A.4
plt.loglog(h,[hi**2 for hi in h])
# %%
