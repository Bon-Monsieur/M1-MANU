import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.sparse as sp

# Définition de la fonction
I = lambda v: 1- 2*np.linalg.norm(np.array([0.5-v[0],0.5-v[1]]),np.inf)

# Création de la grille
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)
Z = np.array([[I([X[i, j], Y[i, j]]) for j in range(X.shape[1])] for i in range(X.shape[0])])

# Tracé de la surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='spring')

# Étiquettes des axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('I(X, Y)')

Nx = Ny = 5
Un = np.full((Nx, Ny), 1.0)  # U0 == 0
Un[0,:]= 2
print(Un)