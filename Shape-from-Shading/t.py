import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Définition du domaine
x_min, x_max = 0,1
y_min, y_max = 0,1
nb_pixels = 21
x = np.linspace(x_min, x_max, nb_pixels)
y = np.linspace(y_min, y_max, nb_pixels)
X, Y = np.meshgrid(x, y)
print(x[10],y[10])
print(len(x))
Z = 1
# Tracé en 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('U_SV')
ax.set_title('Image synthétique du vase en 3D')
plt.show()
