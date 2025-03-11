import numpy as np
import matplotlib.pyplot as plt

# Définition de la fonction
I = lambda v: 1 / np.sqrt(1 + (16 * v[1] * (1 - v[1]) * (1 - 2 * v[0]))**2 + (16 * v[0] * (1 - v[0]) * (1 - 2 * v[1]))**2)

# Définition du maillage
x = np.linspace(0, 1, 41)
y = np.linspace(0, 1, 41)
X, Y = np.meshgrid(x, y)

# Calcul des valeurs de I sur le maillage
Z = np.array([[I([X[i, j], Y[i, j]]) for j in range(X.shape[1])] for i in range(X.shape[0])])

# Tracé du graphique
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, Z, levels=50, cmap='viridis')
plt.colorbar(contour, label='I(v)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Tracé de la fonction I(v)')
plt.show()