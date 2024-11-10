# %%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
import threading
import time as pytime
from plot_solution import plot_progression_with_controls

def schema_chaleur2D(u0, mesh_dimensions, T, D=2.2e-5, CFL=1, every=1):
    m, p = mesh_dimensions
    if p < 1 or m < 1:
        print("Incorrect mesh dimensions")
        return None
    dx = 1 / (m - 1)
    dy = 1 / (p - 1)
    dt = CFL * (dx**2 * dy**2) / (2 * D * (dx**2 + dy**2))  # Condition CFL
    lx = D * dt / dx**2
    ly = D * dt / dy**2

    x = np.linspace(0, 1.0, m)
    y = np.linspace(0, 1.0, p)
    X, Y = np.meshgrid(x, y, indexing="ij")
    Uh = u0(X, Y)
    t = 0
    it = 0
    Uh_history = [(t, Uh.copy())]

    while t < T:
        it += 1
        if T - t < dt:
            dt = T - t
            lx = D * dt / dx**2
            ly = D * dt / dy**2
        t += dt
        Uh[1:-1, 1:-1] = (
            Uh[1:-1, 1:-1]
            + lx * (Uh[2:, 1:-1] + Uh[:-2, 1:-1] - 2 * Uh[1:-1, 1:-1])
            + ly * (Uh[1:-1, 2:] + Uh[1:-1, :-2] - 2 * Uh[1:-1, 1:-1])
        )
        Uh[0, :] = Uh[-1, :] = Uh[:, 0] = Uh[:, -1] = 0.0  # Apply boundary conditions

        # Store every iteration
        if it % every == 0:
            Uh_history.append((t, Uh.copy()))

    return Uh, Uh_history



def u0(x, y):
    # Initial condition: set to 1 if within the region [0.4, 0.6] x [0.4, 0.6], else 0
    return np.where((0.4 <= x) & (x <= 0.6) & (0.4 <= y) & (y <= 0.6), 2.0, 0.0)



# Run the simulation
T = 300
D = 2.2e-5  # Thermal diffusivity of air in m^2/s
mesh_dimensions = (40, 40)
CFL = 0.45
final_temperature_distribution, Uh_history = schema_chaleur2D(
    u0, mesh_dimensions, T=T, D=D, CFL=CFL, every=5
)

# Generate the grid for plotting
m, p = mesh_dimensions
x = np.linspace(0, 1, m)
y = np.linspace(0, 1, p)
X, Y = np.meshgrid(x, y)

# Plot the progression of temperature distributions with interactive controls
plot_progression_with_controls(Uh_history, X, Y, plot_type='3d')

# %%
