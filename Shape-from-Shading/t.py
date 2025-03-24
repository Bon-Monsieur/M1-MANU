import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import lu_factor, lu_solve, cho_factor, cho_solve

# Fonction de base en chapeau
def phi(i, x, X):
    h = X[1] - X[0]
    return np.where((X[i-1] <= x) & (x <= X[i]), (x - X[i-1])/h,
           np.where((X[i] <= x) & (x <= X[i+1]), (X[i+1] - x)/h, 0))

# Fonction principale des éléments finis
def finite_elements(N=50, f=np.exp, method="trapeze"):
    
    # Maillage
    X = np.linspace(0, 1, N+2)  # N points intérieurs + conditions limites
    h = X[1] - X[0]

    # Définition de l'intégrale source G
    if method == "trapeze":
        def l(i):
            return h/2 * (f(X[i-1]) + f(X[i+1]))  # Formule du trapèze
    elif method == "simpson":
        def l(i):
            return h/6 * (f(X[i-1]) + 4*f((X[i-1]+X[i+1])/2) + f(X[i+1]))  # Simpson
    elif method == "point_milieu":
        def l(i):
            return h * f((X[i-1]+X[i+1])/2)  # Point milieu

    # Construction de la matrice de rigidité K
    K = (np.eye(N) * 2 + np.diag([-1]*(N-1), 1) + np.diag([-1]*(N-1), -1)) / h
    
    # Second membre du système
    G = np.array([l(i) for i in range(1, N+1)])

    # Résolution du système avec Cholesky (plus stable)
    L = cho_factor(K, lower=True)
    U = cho_solve(L, G)

    # Ajout des conditions aux limites
    U = np.concatenate(([0], U, [0]))

    # Solution exacte pour f(x) = exp(x)
    def exact(x):
        return -np.exp(x) + (-1+np.exp(1))*x + 1

    # Calcul de l'erreur sur les points internes
    err = np.mean(np.abs(U[1:-1] - exact(X[1:-1])))
    print(f"Erreur moyenne : {err:.2e}")

    # Affichage des solutions
    plt.plot(X, exact(X), label='Solution exacte', linewidth=2)
    plt.plot(X, U, '--', label='Solution approchée')
    plt.legend()
    plt.show()

# Fonction test
def f1(x):
    return np.exp(x)

# Appel de la fonction
finite_elements(N=1000, f=f1, method="point_milieu")
