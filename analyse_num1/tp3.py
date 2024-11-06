#%%
import numpy as np
import matplotlib.pyplot as plt 
# %%

a = 0
b = 3
alpha = -5
beta = 3 
nint = 20

h = (b-a)/nint
x = np.arange(a,b+h,h)

#print(x)
print(len(x))

def poisson1D(x,f):
    
    A = -2*np.identity(len(x)-1)
    b = [1]*(len(x)-2)
    np.fill_diagonal(A[1:],b)
    np.fill_diagonal(A[:,1:],b)
    A[0,0] = -3/2
    A[0,1] = 2
    A[0,2] = -1/2
    
    A = A*(1/h**2)
    #print(A.shape)
    
    F = [0]
    for i in range(1,len(x)-1):
        F.append(f(x[i]))
    #print(len(F))
    
    Bc = np.zeros(len(x)-1)
    Bc[0] = alpha/h
    Bc[-1] = -beta/h**2

    Uh = np.linalg.inv(A).dot(F+Bc)
    Uh = np.append(Uh,beta)
    print(Uh)
    return Uh

# Solution approchée
Uh = poisson1D(x,np.exp)

#Solution analytique
v = np.linspace(a,b,100)

def f(x):
    return np.exp(x)-np.exp(b) + (alpha-np.exp(a))*(x-b) + beta

fv = [f(x) for x in v]

# Création du graphique
plt.plot(x, Uh, marker='.') 
plt.title("Solution numérique avec 21 points")
plt.plot(v, fv, marker='.') 

# Affichage
plt.show()


# Calcul de l'erreur
Uex = np.array([f(x) for x in x])
E = Uh - Uex
print(E)


# %%
