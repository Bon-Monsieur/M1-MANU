import numpy as np
import matplotlib.pyplot as plt

def compute_U(shape, dx, dy, phi, N, tol=1e-6, max_iter=1000):
    """
    Approximation numérique de l'équation de Hamilton-Jacobi avec différences finies.
    
    :param shape: (Nx, Ny) dimensions de la grille
    :param dx: pas spatial en x
    :param dy: pas spatial en y
    :param phi: fonction initiale sur le bord
    :param N: matrice des valeurs N_{ij}
    :param tol: tolérance pour la convergence
    :param max_iter: nombre maximal d'itérations
    :return: matrice U approximant la solution
    """
    Nx, Ny = shape
    U = np.full((Nx, Ny), np.inf)  # Initialisation avec des grandes valeurs
    
    # Appliquer la condition initiale
    for i in range(Nx):
        for j in range(Ny):
            if phi[i, j] is not None:
                U[i, j] = phi[i, j]
    
    for iteration in range(max_iter):
        U_old = U.copy()
        
        for i in range(1, Nx-1):
            for j in range(1, Ny-1):
                if phi[i, j] is None:  # Ne pas modifier les points de bord
                    D_x_minus = (U[i, j] - U[i-1, j]) / dx
                    D_x_plus = (U[i+1, j] - U[i, j]) / dx
                    D_y_minus = (U[i, j] - U[i, j-1]) / dy
                    D_y_plus = (U[i, j+1] - U[i, j]) / dy
                    
                    g_val = np.sqrt(max(D_x_minus, 0)**2 + max(D_x_plus, 0)**2 + 
                                    max(D_y_minus, 0)**2 + max(D_y_plus, 0)**2) - N[i, j]
                    
                    if g_val > 0:
                        U[i, j] = min(U[i, j], U_old[i, j] - g_val)
        
        # Condition d'arrêt si convergence
        if np.linalg.norm(U - U_old, ord=np.inf) < tol:
            break
    
    return U

# Exemple d'utilisation avec une image simulant l'illumination d'un vase
Nx, Ny = 100, 100
phi = np.full((Nx, Ny), None)  # Valeurs None sauf sur le bord
phi[:, 0] = 1  # Bord gauche
phi[:, -1] = 0  # Bord droit
N = np.ones((Nx, Ny))  # Valeur arbitraire pour N

# Simuler une illumination avec un gradient
for j in range(Ny):
    phi[Nx//3:2*Nx//3, j] = np.cos(j / Ny * np.pi)  # Simulation de lumière

U = compute_U((Nx, Ny), dx=0.1, dy=0.1, phi=phi, N=N)

# Affichage de l'image
plt.imshow(U, cmap='gray', origin='lower')
plt.colorbar(label='Approximation de la forme')
plt.title('Approximation d’un vase éclairé')
plt.show()
