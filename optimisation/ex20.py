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

proj = p0 + p1 + p2   #Tableau des coefs de la projection

# Définition du polynômes de la projection à partir de ses coefs
def proj_poly(x): 
    l = [proj[i]*x**i for i in range(len(proj))]
    return sum(l)

#Définition de f-p(f)
def test(x):
    return f(x)-proj_poly(x)

# Affiche les coefs de la projection de x^3 
print(proj)
print(produit_scalaire(test,test))
print(4/175)
print(2/5/np.sqrt(7),np.sqrt(4/175))


def coef_to_poly(l,x):
    res = [l[i]*x**i for i in range(len(l))]
    return sum(res)


def projection_poly(f): # f est un tableau de ses coefs

    # Coefs de la base dans laquelle on veut projeter f
    coefs_Q0 = np.array([1,0,0])
    coefs_Q1 = np.array([0,np.sqrt(3),0])
    coefs_Q2 = np.array([np.sqrt(5)/2,0,-3*np.sqrt(5)/2])

    # Calcul du produit_scalaire de f et tous les Qi
    x = [-1 + (i-1)*delta for i in range(1,N+1)]

    prod0 = sum([delta*coef_to_poly(f,x[i])*coef_to_poly(coefs_Q0,x[i])/2 for i in range(len(x))])
    prod1 = sum([delta*coef_to_poly(f,x[i])*coef_to_poly(coefs_Q1,x[i])/2 for i in range(len(x))])
    prod2 = sum([delta*coef_to_poly(f,x[i])*coef_to_poly(coefs_Q2,x[i])/2 for i in range(len(x))])
    
    p0 = prod0 * coefs_Q0
    p1 = prod1 * coefs_Q1
    p2 = prod2 * coefs_Q2

    proj = p0+p1+p2

    return proj

print(projection_poly([0,0,0,1]))

# %%
