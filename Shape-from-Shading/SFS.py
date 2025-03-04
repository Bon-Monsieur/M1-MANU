#%%
import numpy as np
import matplotlib.pyplot as plt
# %%
global I
def n(I,v):
    return np.sqrt(1/I(v)**2-1)

def N(I,i,j):
    return n(I,[x[i],y[i]])

nb_pt = 21
x = np.linspace(0,1,nb_pt)
y = np.linspace(0,1,nb_pt)
X,Y = np.meshgrid(x,y)
Dx = x[1]-x[0]
Dy = y[1]-y[0]
Dt = Dx*Dy/np.sqrt(Dx**2+Dy**2)
tau = Dt


def Dxp(U,i,j):
    return (U[i+1,j]-U[i,j])/Dx

def Dxm(U,i,j):
    return (U[i,j]-U[i-1,j])/Dx

def Dyp(U,i,j):
    return (U[i,j+1]-U[i,j])/Dy

def Dym(U,i,j):
    return (U[i,j]-U[i,j-1])/Dy
     
def g(i,j,a,b,c,d):
    return np.sqrt(max(a,b)**2+max(c,d)**2) - N(I,i,j)

def phi(v):
    x,y=v
    return 0


def G(U,i,j):
    return g(i,j,Dxm(U,i,j),Dxp(U,i,j),Dym(U,i,j),Dyp(U,i,j))
# %%
