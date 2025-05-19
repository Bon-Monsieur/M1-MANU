import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # utile pour la projection 3D

# Grille
Nx, Ny = 100, 100
x = np.linspace(-0.5, 0.5, Nx)
y = np.linspace(-0.5, 0.5, Ny)
X, Y = np.meshgrid(x, y)

# Fonction g(x)
g = lambda x, y: (-np.cos(2 * np.pi * x) * np.cos(2 * np.pi * y) + np.sin(2 * np.pi * x) * np.sin(2 * np.pi * y))
Z = g(X,Y)

# Tracé 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, color='white', edgecolor='black', alpha=0.95)

ax.set_title(r'$f(x, y) = \sqrt{g(x)^2 - y^2}$', fontsize=14)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
plt.tight_layout()
plt.show()
