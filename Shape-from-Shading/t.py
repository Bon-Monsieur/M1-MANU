import numpy as np
import matplotlib.pyplot as plt

# Définition de g(x)
def g(x):
    return 0.15 - 0.025 * (6*x - 1) * (2*x - 1)**2 * (3*x + 2)**2 * (2*x + 1)

# Approximation numérique de la dérivée de g(x)
def dg_dx(x, dx=1e-5):
    return (g(x + dx) - g(x - dx)) / (2 * dx)

# Définition de la fonction z(x, y)
def z(x, y):
    val = g(x)**2 - y**2
    return np.sqrt(val) if val >= 0 else np.nan  # Éviter les valeurs complexes

# Définition des dérivées partielles de z
def dz_dx(x, y):
    val = g(x)**2 - y**2
    return (g(x) * dg_dx(x)) / np.sqrt(val) if val > 0 else np.nan

def dz_dy(x, y):
    val = g(x)**2 - y**2
    return -y / np.sqrt(val) if val > 0 else np.nan

# Fonction f(x, y)
def f(x, y):
    grad_x = dz_dx(x, y)
    grad_y = dz_dy(x, y)
    return 1 / np.sqrt(1 + grad_x**2 + grad_y**2) if not np.isnan(grad_x) and not np.isnan(grad_y) else np.nan

# Création de la grille de points
x_vals = np.linspace(-0.5, 0.5, 256)
y_vals = np.linspace(-0.5, 0.5, 256)
X, Y = np.meshgrid(x_vals, y_vals)

# Calcul des valeurs de f(x, y)
F = np.vectorize(f)(X, Y)

# Seuil pour détecter les valeurs proches de 1
threshold = 1e-4
mask = np.abs(F - 1) < threshold

# Sélection des indices uniques où f(x, y) ≈ 1
X_points = X[mask]
Y_points = Y[mask]

# Éviter trop de points rouges en en prenant un seul par cluster (espacement)
if len(X_points) > 0:
    X_selected = X_points[::]  # Prendre 1 point tous les 10 pour éviter trop de superposition
    Y_selected = Y_points[::]
else:
    X_selected = []
    Y_selected = []

# Tracé de la fonction en 2D
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, F, levels=50, cmap='viridis')
plt.colorbar(label="1 / sqrt(1 + |∇z|²)")

# Ajout des points rouges uniques aux endroits où f(x, y) ≈ 1
plt.scatter(X_selected, Y_selected, color='red', s=20, marker='o', label="f(x,y) ≈ 1")

# Étiquettes et titre
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Tracé de 1 / sqrt(1")
plt.legend()
plt.show()
