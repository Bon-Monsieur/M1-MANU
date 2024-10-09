#%%
import numpy as np
import matplotlib.pyplot as plt

# %%

# Nombres de points
N=10000

# Distance entre les points
delta = 2/(N-1)

# Les points xi où on  évalue les fonctions
x = [-1 + (i-1)*delta for i in range(1,N+1)]

# Coefficients des polynômes Q0, Q1, Q2
coefs_Q0 = np.array([1,0,0])
coefs_Q1 = np.array([0,np.sqrt(3),0])
coefs_Q2 = np.array([np.sqrt(5)/2,0,-3*np.sqrt(5)/2])

# Définitions des polynômes
def f(x):
    return x**3

def Q0(x):
    return 1

def Q1(x):
    return np.sqrt(3)*x

def Q2(x):
    return x**2*(-3*np.sqrt(5)/2)+np.sqrt(5)/2


def produit_scalaire(f,g):
    l = [delta*f(x[i])*g(x[i])/2 for i in range(len(x))]
    return sum(l)

p0 = produit_scalaire(f,Q0) * coefs_Q0
p1 = produit_scalaire(f,Q1) * coefs_Q1
p2 = produit_scalaire(f,Q2) * coefs_Q2

proj = p0 + p1 + p2

print(proj)
#print(produit_scalaire(Q2,Q2))

# %%
