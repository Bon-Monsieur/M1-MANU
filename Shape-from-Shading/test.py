import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Définir la fonction I(x, y)
def I(x, y):
    return 1 / np.sqrt(1 + (2 * np.pi * np.sin(2 * np.pi * y) * np.cos(2 * np.pi * x))**2 + (2 * np.pi * np.sin(2 * np.pi * x) * np.cos(2 * np.pi * y))**2)

# Créer une grille de points (x, y)
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)

# Calculer les valeurs de la fonction sur la grille
Z = I(X, Y)

# Créer la figure 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Tracer la surface 3D
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

# Ajouter une barre de couleur
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='I(x, y)')

# Ajouter des labels
ax.set_title('Visualisation 3D de la fonction I(x, y)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('I(x, y)')

# Afficher le graphique
plt.show()