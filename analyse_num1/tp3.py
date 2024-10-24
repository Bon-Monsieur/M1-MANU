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



def poisson1D(x,f):
    
    A = -2*np.identity(len(x)-2)
    b = [1]*(len(x)-2)
    np.fill_diagonal(A[1:],b)
    np.fill_diagonal(A[:,1:],b)
    
    A = A*(1/h**2)
    
    F = np.array([f(x[i]) for i in range(1,len(x)-1)])
   
    Bc = np.zeros(len(x)-2)
    Bc[0] = alpha/h**2
    Bc[-1] = beta/h**2
    
    Uh = np.dot(np.linalg.inv(A),(F+Bc))
    
    Uh = np.insert(Uh, 0, alpha)
    Uh = np.append(Uh, beta)
    

    return Uh


Uh = poisson1D(x,np.exp)
plt.scatter(x,Uh,marker='.')

# %%
