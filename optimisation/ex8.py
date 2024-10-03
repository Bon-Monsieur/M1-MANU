#%%
import numpy as np
import matplotlib.pyplot as plt

# %%

def C(x,y):
    return x**4 -2*x**2 + y**2 -3 

# Générer une grille de points dans R²
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)

# Calculer f(x, y) sur cette grille
Z = C(X, Y)

# Tracer la frontière où f(x, y) = 0 (cercle de rayon 1)
plt.contour(X, Y, Z, levels=[0], colors='red')
plt.title("Frontière définie par C(x, y) = 0")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()
# %%
