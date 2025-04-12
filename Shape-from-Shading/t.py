import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Définir le polynôme P(bar_x)
def P(bar_x):
    return (-138.24 * bar_x**6 +
             92.16 * bar_x**5 +
             84.48 * bar_x**4 -
             48.64 * bar_x**3 -
             17.60 * bar_x**2 +
              6.40 * bar_x +
              3.20)

# Définir u_SV(x, y) en évitant les racines négatives
def u_sv(x, y):
    bar_x = x / 12.8
    p_val = P(bar_x)
    result = np.zeros_like(x)
    mask = p_val**2 >= y**2
    result[mask] = np.sqrt(p_val[mask]**2 - y[mask]**2)
    return result

# Domaine pour x et y
x_vals = np.linspace(-6.4, 6.4, 300)
y_vals = np.linspace(-5, 5, 300)
X, Y = np.meshgrid(x_vals, y_vals)
Z = u_sv(X, Y)

# Tracé 3D
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, antialiased=True)

ax.set_title('Surface 3D de $u_{SV}(x, y)$')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('$u_{SV}(x, y)$')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='$u_{SV}$')
plt.show()
