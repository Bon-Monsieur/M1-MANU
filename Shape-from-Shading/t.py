import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Définition de la fonction
I  = lambda v: np.sin(2*np.pi*v[0])*np.sin(2*np.pi*v[1])

# Création de la grille
x = np.linspace(0, 1, 21)
y = np.linspace(0, 1, 21)
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


plt.show()