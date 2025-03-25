import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import lu_factor, lu_solve, cho_factor, cho_solve

def phi(i, x, X):
    h = X[1] - X[0]
    return np.where((X[i-1] <= x) & (x <= X[i]), (x - X[i-1])/h,
           np.where((X[i] <= x) & (x <= X[i+1]), (X[i+1] - x)/h, 0))
#plt.plot(np.linspace(0, 1, 11), [phi(1, x, np.linspace(0, 1, 11)) for x in np.linspace(0, 1, 11)])
 


def finite_elements1D(N=50, f=np.exp,method="trapeze",algo="LU"):
    
    # Maillage
    X = np.linspace(0, 1, N+2)
    h = X[1] - X[0]
    
    
    # Chaque intégrales est calculée en 2 parties
    if method == "point_milieu":
        def l(i):
            return  (X[i+1] - X[i]) * f((X[i+1]+X[i])/2) * phi(i, (X[i+1]+X[i])/2,X) + (X[i] - X[i-1]) * f((X[i]+X[i-1])/2) * phi(i, (X[i]+X[i-1])/2,X)
    elif method == "trapeze": 
        def l(i):
            return  (X[i+1] - X[i])/2 * ( (f(X[i+1]) * phi(i, X[i+1],X)) + (f(X[i]) * phi(i, X[i],X)) ) + (X[i] - X[i-1])/2 * ( (f(X[i]) * phi(i, X[i],X)) + (f(X[i-1]) * phi(i, X[i-1],X)) )
    elif method == "simpson":
        def l(i):
            return  (X[i+1] - X[i])/6 * (f(X[i+1]) * phi(i, X[i+1],X) + 4*f((X[i+1]+X[i])/2) * phi(i, (X[i+1]+X[i])/2,X) + f(X[i]) * phi(i, X[i],X)) + (X[i] - X[i-1])/6 * (f(X[i]) * phi(i, X[i],X) + 4*f((X[i]+X[i-1])/2) * phi(i, (X[i]+X[i-1])/2,X) + f(X[i-1]) * phi(i, X[i-1],X))
    
    

    K = (np.identity(N)*2 + np.diag([-1]*(N-1), 1) + np.diag([-1]*(N-1), -1))/h         # Matrice de a
    G = [l(i) for i in range(1,N+1)]
    

    if algo == "LU":
        U = np.linalg.solve(K, G)
    elif algo == "Cholesky":
        # Décomposition de Cholesky
        L = cho_factor(K, lower=True)
    
        # Résolution du système
        U = cho_solve(L, G)
        
    

    # Ajout des conditions aux limites pour affichage
    U = np.concatenate(([0], U, [0]))

    # Solution exacte pour f(x) = exp(x)
    def exact(x):
        return -np.exp(x) + (-1+np.exp(1))*x + 1
    plt.plot(np.linspace(0,1,N), exact(np.linspace(0,1,N)), label='Solution exacte')
    
    # Calcul de l'erreur
    err = np.mean(np.abs(U[1:-1] - exact(X)[1:-1]))
    print(err)
    
    plt.plot(X, U, label='Solution approchée')
    plt.title(f"Éléments finis avec {N} points")
    plt.legend()
    plt.show()


def f1(x):
    return np.exp(x)

finite_elements1D(N=15, f=f1,method="trapeze",algo="LU")

