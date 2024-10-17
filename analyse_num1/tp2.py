#%%
import numpy as np
import math
import matplotlib.pyplot as plt 
#%%

# Question 1
# Matrice de Vandermonde correspondant au système à résoudre
A = np.array([[1,1,1,1],
             [-2,-1,1,2],
             [4/2,1/2,1/2,4/2],
             [-8/6,-1/6,1/6,8/6]])

b = np.array([0,0,0,1])

X = np.linalg.solve(A, b)

print(X)
# [-0.5 1 -1 0.5]

# %%
# Question 2 


def CoefDF(k, xbar, pt):
    n = len(pt) # Taille de la matrice

    # Définition du vecteur b = (0,..,0,1,0,..,0) avec 1 à la k-ieme coord
    b = [0]*n  
    b[k] = math.factorial(k)

    # Définition de la matrice qui sert à trouver les coefs
    A = np.vander(pt, n, increasing=True).T
    
    # Résoudre le système AX=b
    C = np.linalg.solve(A,b)

    return C


# %%
# Question 3

# Retrouver les valeurs de la question 1 

k = 3 
xbar = 0
h = 1 
pt = np.array([xbar-2*h,xbar-h,xbar+h,xbar+2*h])

print(CoefDF(3,xbar,pt))

# Trouver les coefs pour k=4
k = 4
xbar = 1
pt = np.array([xbar-2*h,xbar-h,xbar,xbar+h,xbar+2*h])
C = CoefDF(k=4,xbar=1,pt=pt)
print(C)
# La méthode est précise d'ordre 1 ? 

h = [5e-1, 10e-2, 5e-2, 10e-3, 5e-3]

def u(x):
    return np.sin(x)

def formule(h,xbar):
    pt = np.array([xbar-2*h,xbar-h,xbar,xbar+h,xbar+2*h])
    l= [C[i]*np.sin(pt[i])/h**4 for i in range(len(pt))]
    return sum(l)

tau = [np.abs(formule(h,xbar)-np.sin(1)) for h in h] 
plt.loglog(h,tau,label='Tau')
plt.legend()
plt.show()


#%%
