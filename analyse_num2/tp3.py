#%%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
import threading
import time as pytime
from plot_solution import plot_progression_with_controls

# Constantes données dans l'énoncé
Text = 5.0
Trad = 40.0

# La fonction phi demandée, qui calcule la chaleur à rajouter si on se trouve dans le radiateur
def phi(x,y,val):
    if (0.1<=x<=0.2) and (0.4<=y<=0.6):
        return (Trad - val)**3
    else:
        return 0



def schema_chaleur2D_explicite(u0, mesh_dimensions, T, D=1, CFL=0.4,Nt_print_max=10):
    m, p = mesh_dimensions
    if p < 1 or m < 1:
        print("Incorrect mesh dimensions")
        return None

    # Les constantes que l'on va utiliser pour faire les calcules
    dx = 1 / (m - 1)
    dy = 1 / (p - 1)
    dt = CFL * (dx**2 * dy**2) / (2 * D * (dx**2 + dy**2))  # Condition CFL
    #print(np.floor(T/dt))
    lx = D * dt / dx**2
    ly = D * dt / dy**2
    
    # Discrétisation de l'espace (création du mesh)
    x = np.linspace(0, 1.0, m)
    Nx = len(x)
    y = np.linspace(0, 1.0, p)
    Ny = len(y)
    X, Y = np.meshgrid(x, y, indexing="ij")
    Uh = np.zeros((m,p))


    # Initialisation au temps t=0 avec u(x,t) = x0(x)
    for i in range(Nx):
        for j in range(Ny):
            Uh[i,j] = u0(x[i],y[j])
    #print(Uh)

    t = 0
    it = 0

    dt_print = T/(Nt_print_max-1)

    Uh_history = [(t, Uh.copy())]
    uold=Uh

    while t < T:
        it += 1
        if T - t < dt:
            dt = T - t
            lx = D * dt / dx**2
            ly = D * dt / dy**2
        t += dt
        for i in range(1, m-1):
            for j in range(1, p-1):
                Uh[i, j] = (1 - 2 * (lx + ly)) * uold[i, j] + \
                           lx * (uold[i + 1, j] + uold[i - 1, j]) + \
                           ly * (uold[i, j + 1] + uold[i, j - 1]) + \
                           dt * phi(x[i],y[j],uold[i,j])
        uold[:]=Uh[:]
        
        # Apply boundary conditions without corners
        Uh[0, 1:-1] = Uh[1, 1:-1] 
        Uh[-1, 1:-1] = Uh[-2, 1:-1]
        Uh[1:-1,0] = Uh[1:-1,1]
        Uh[1:-1,-1] = Uh[1:-1,-2]

        # Calculer les coins
        Uh[0,0] = (Uh[0,1]+Uh[1,0])/2
        Uh[-1,0] = (Uh[-1,1]+Uh[-2,0])/2
        Uh[0,-1] = (Uh[0,-2]+Uh[1,-1])/2
        Uh[-1,-1] = (Uh[-1,-2]+Uh[-2,-1])/2

        # Remettre la fenetre dans Uh
        for i in range(Nx):
            for j in range(Ny):
                Uh[i,j] = fenetre(x[i],y[j],Uh[i,j])

    
        # Store Nt_print_max iterations
        if it % ((T//dt)//Nt_print_max) == 0:
            Uh_history.append((t, Uh.copy()))
        
        #print(len(Uh_history))
    Uh_history.append((t, Uh.copy())) #Save la solution au temps final T
    # End while 
    return Uh, Uh_history


# La température vaut 20 degrés partout sauf aux coordonnées de la fenêtre
def u0(x, y):
    if ((x==0) and (0.4 <= y) and (y <= 0.6)):
        return 5
    else:
        return 20

def fenetre(x,y,val):
    if ((x==0) and (0.4 <= y) and (y <= 0.6)):
        return 5
    else:
        return val

# Run the simulation
T = 1
D = 1  # Thermal diffusivity of air in m^2/s
mesh_dimensions = (40,40)
CFL = 0.45
final_temperature_distribution, Uh_history = schema_chaleur2D_explicite(
    u0, mesh_dimensions, T=T, D=D, CFL=CFL, Nt_print_max=20
)

# Generate the grid for plotting
m, p = mesh_dimensions
x = np.linspace(0, 1, m)
y = np.linspace(0, 1, p)
X, Y = np.meshgrid(x, y)

# Plot the progression of temperature distributions with interactive controls
plot_progression_with_controls(Uh_history, X, Y, plot_type='3d')


# %%
