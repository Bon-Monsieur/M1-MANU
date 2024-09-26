#%%
import numpy as np
import matplotlib.pyplot as plt

# %%
# Définition de la forme quadratique demandée et son gradient

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
    #print(fp)
    return fp

#%%

# Méthode de descente à pas fixe
def descente(grad, x_init, gamma, maxiter, epsilon): 
    x = x_init
    results = [x]
    A = hilbert_matrix(ndim)
    iter = 1

    
    while(iter<maxiter and np.linalg.norm(grad(x)) >= epsilon):
        g = grad(x)
        x = x-gamma*g
        results.append(x)
        iter +=1
    return results,iter


q1 = descente(grad=funcp_axb,x_init=[3]*ndim,gamma=0.1,maxiter=10000,epsilon=1e-3)
print("Dernier des itérés: ",q1[0][-1])    
print("Nb itérations: ",q1[1])

# Afficher les coordonnées du dernier itérés et l'objectif
plt.plot(q1[0][-1],'o-')
plt.plot([1]*ndim)
plt.show()


# %%
# Méthode du gradient à pas optimal pour une forme quadratique


def descente_opti(grad, x_init, maxiter,epsilon): 
    x = x_init
    results = [x]
    A = hilbert_matrix(ndim)
    iter = 1

    hist_grad = []

    while(iter<maxiter and np.linalg.norm(grad(x)) >= epsilon):
        g = grad(x)
        hist_grad.append(g)       # Stocker la valeur du gradient 
        gamma = np.dot(g,g)/np.dot(A.dot(g),g) # Calcul du pas optimal 
        x = x-gamma*g
        results.append(x)
        iter +=1
    return results, iter, hist_grad

q2 = descente_opti(grad=funcp_axb,x_init=[3]*ndim,maxiter=10000,epsilon=1e-3)
print("Dernier des itérés: ",q2[0][-1]) 
print("nombre d'itération :",q2[1])

# Afficher les coordonnées du dernier itérés et l'objectif
plt.plot(q2[0][-1],'o-')
plt.plot([1]*ndim)
plt.show()


liste_dot_grad = [np.dot(q2[2][i],q2[2][i+1]) for i in range(len(q2[2])-1)] # <grad(x_k),grad(x_k+1)>

# Afficher en échelle logarithmique 
#la valeur des produits scalaires des gradients qui tend vers 0
plt.plot(np.log10(np.abs(l1))) 
plt.show()

# %%
