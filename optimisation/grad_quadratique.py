#%%
import numpy as np
import matplotlib.pyplot as plt


# %%

ndim = 20

def hilbert_matrix(n):
    """Renvoie une matrice de Hilbert de taille n x n."""
    H = np.zeros((n, n))  # Créer une matrice n x n remplie de zéros
    for i in range(n):
        for j in range(n):
            H[i, j] = 1 / (i + j + 1)  # Les indices commencent à 0, donc ajouter 1
    return H

def func_axb(x):
    A = hilbert_matrix(ndim)
    xcible = np.ones(ndim)
    b = A.dot(xcible)
    J = 0.5*(A.dot(x)).dot(x)-b.dot(x)
    return J

def funcp_axb(x):
    A = hilbert_matrix(ndim)
    xcible = np.ones(ndim)
    b = A.dot(xcible)
    fp = A.dot(x)-b
    print(fp)
    return fp


def descente(grad, x_init, gamma, maxiter, epsilon): #Methode de descente du tp note
    x = x_init
    results = [x]
    for i in range(1, maxiter + 1):
        g = grad(x)
        if np.linalg.norm(g) <= epsilon:
            break
        else:
            x = x-gamma*g
            results.append(x)
    return results

q1 = descente(grad=funcp_axb,x_init=[3]*ndim,gamma=0.1,maxiter=100,epsilon=1e-10)
print("Liste des itérés: ",q1)
print("Dernier des itérés: ",q1[-1])    

plt.plot(q1[-1])
plt.plot([1]*ndim)
plt.show()
# %%
