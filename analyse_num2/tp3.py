#%%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
import threading
import time as pytime
from plot_solution import plot_progression_with_controls
'''
# Constantes données dans l'énoncé
Text = 5.0
Trad = 40.0

# La fonction phi demandée, qui calcule la chaleur à rajouter si on se trouve dans le radiateur
def phi(Uh, X, Y):
    # Masques pour les conditions spatiales
    mask = (0 <= X) & (X <= 0.1) & (0.4 <= Y) & (Y <= 0.6)
    # Appliquer la condition de phi
    result = np.zeros_like(Uh)
    result[mask] = (Trad - Uh[mask])**3
    return result


def fenetre(Uh, X, Y):
    # Masques pour les conditions spatiales
    mask = (X == 0) & (0.4 <= Y) & (Y <= 0.6)
    # Modifier les valeurs dans Uh uniquement là où le masque est vrai
    Uh[mask] = 5
    return Uh




def schema_chaleur2D_explicite(mesh_dimensions, T, D=1, CFL=0.45,Nt_print_max=10):
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
    y = np.linspace(0, 1.0, p)
    X, Y = np.meshgrid(x, y, indexing="ij")

    # Initialisation au temps t=0 avec u(x,t) = x0(x) de manière vectorisée
    Uh = np.full((m, p), 20.0)  # Initialiser tout à 20°C
    mask_fenetre = (X == 0) & (0.4 <= Y) & (Y <= 0.6)  # Détecter la fenêtre
    Uh[mask_fenetre] = 5  # Appliquer la condition de la fenêtre


    t = 0
    it = 0

    # Variable d'affichage des solutions 
    dt_print = T/(Nt_print_max-1)

    # Historique des solutions 
    Uh_history = [(t, Uh.copy())]
    uold=Uh

    while t < T:
        it += 1

        # Dernière itération
        if T - t < dt:
            dt = T - t
            lx = D * dt / dx**2
            ly = D * dt / dy**2

        t += dt

        Uh[1:-1, 1:-1] = (
            Uh[1:-1, 1:-1]
            + lx * (Uh[2:, 1:-1] + Uh[:-2, 1:-1] - 2 * Uh[1:-1, 1:-1])
            + ly * (Uh[1:-1, 2:] + Uh[1:-1, :-2] - 2 * Uh[1:-1, 1:-1])
            + dt * phi(Uh[1:-1, 1:-1], X[1:-1, 1:-1], Y[1:-1, 1:-1])
            )

        
        # Apply boundary conditions without corners (order = 2)
        Uh[0, 1:-1] = 4/3*Uh[1, 1:-1] -1/3*Uh[2,1:-1]
        Uh[-1, 1:-1] = 4/3*Uh[-2, 1:-1] -1/3*Uh[-3,1:-1]
        Uh[1:-1,0] = 4/3*Uh[1:-1,1] - 1/3*Uh[1:-1,2]
        Uh[1:-1,-1] = 4/3*Uh[1:-1,-2] - 1/3*Uh[1:-1,-3]
        
        
        # Calculer les coins (order = 2)
        Uh[0,0] = (4/3*Uh[0,1]-1/3*Uh[0,2] + 4/3*Uh[1,0] - 1/3*Uh[2,0])/2
        Uh[-1,0] = (4/3*Uh[-2,0]-1/3*Uh[-3,0] + 4/3*Uh[-1,1] - 1/3*Uh[-1,2])/2
        Uh[0,-1] = (4/3*Uh[0,-2]-1/3*Uh[0,-3] + 4/3*Uh[1,-1] - 1/3*Uh[2,-1])/2
        Uh[-1,-1] = (4/3*Uh[-2,-1]-1/3*Uh[-3,-1] + 4/3*Uh[-1,-2] - 1/3*Uh[-1,-3])/2
        

        # Remettre la fenetre dans Uh
        Uh = fenetre(Uh,X,Y)
    
        # Store Nt_print_max iterations
        if it % ((T//dt)//Nt_print_max) == 0:
            Uh_history.append((t, Uh.copy()))
        
    #Save la solution au temps final T
    Uh_history.append((t, Uh.copy())) 
    
    return Uh, Uh_history



# Run the simulation
T = 1
D = 1  # Thermal diffusivity of air in m^2/s
mesh_dimensions = (50,50)
CFL = 0.45
final_temperature_distribution, Uh_history = schema_chaleur2D_explicite(
    mesh_dimensions, T=T, D=D, CFL=CFL, Nt_print_max=20
)

# Generate the grid for plotting
m, p = mesh_dimensions
x = np.linspace(0, 1, m)
y = np.linspace(0, 1, p)
X, Y = np.meshgrid(x, y)

# Plot the progression of temperature distributions with interactive controls
plot_progression_with_controls(Uh_history, X, Y, plot_type='3d')
'''

# %%
# SCHEMA D'ORDRE 4 EN ESPACE ET 1 EN TEMPS 

# Constantes données dans l'énoncé
Text = 5.0
Trad = 40.0

# La fonction phi demandée, qui calcule la chaleur à rajouter si on se trouve dans le radiateur
def phi(Uh, X, Y):
    # Masques pour les conditions spatiales
    mask = (0.45 <= X) & (X <= 0.55) & (0.4 <= Y) & (Y <= 0.6)
    # Appliquer la condition de phi
    result = np.zeros_like(Uh)
    result[mask] = (Trad - Uh[mask])**3
    return result


def fenetre(Uh, X, Y):
    # Masques pour les conditions spatiales
    mask = (X == 0.0) & (0.4 <= Y) & (Y <= 0.6)
    # Modifier les valeurs dans Uh uniquement là où le masque est vrai
    Uh[mask] = 5
    return Uh




def schema_chaleur2D_explicite_o4(mesh_dimensions, T, D=1, CFL=0.45,Nt_print_max=10):
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
    y = np.linspace(0, 1.0, p)
    X, Y = np.meshgrid(x, y, indexing="ij")
    

    # Initialisation au temps t=0 avec u(x,t) = x0(x) de manière vectorisée
    Uh = np.full((m, p), 20.0)  # Initialiser tout à 20°C
    mask_fenetre = (X == 0) & (0.4 <= Y) & (Y <= 0.6)  # Détecter la fenêtre
    Uh[mask_fenetre] = 5  # Appliquer la condition de la fenêtre


    t = 0
    it = 0

    # Variable d'affichage des solutions 
    dt_print = T/(Nt_print_max-1)

    # Historique des solutions 
    Uh_history = [(t, Uh.copy())]
    uold=Uh.copy()

    while t < T:
        it += 1

        # Dernière itération
        if T - t < dt:
            dt = T - t
            lx = D * dt / dx**2
            ly = D * dt / dy**2

        t += dt

        Uold = Uh.copy()

        # Carre interne du carre interne 
        Uh[2:-2, 2:-2] = (
            Uold[2:-2, 2:-2]
            + lx * ( -1/12*Uold[:-4, 2:-2] + 4/3*Uold[1:-3,2:-2] -2.5 * Uold[2:-2, 2:-2] + 4/3*Uold[3:-1, 2:-2] - 1/12*Uold[4:,2:-2])
            + ly * ( -1/12*Uold[2:-2, :-4] + 4/3*Uold[2:-2,1:-3] -2.5 * Uold[2:-2, 2:-2] + 4/3*Uold[2:-2,3:-1] - 1/12*Uold[2:-2,4:])
            + dt * phi(Uold[2:-2, 2:-2], X[2:-2, 2:-2], Y[2:-2, 2:-2])
            )
        

        # Carre interne sans les 4 coins internes
        Uh[1, 2:-2] = (
            Uold[1, 2:-2]+
            lx * (11/12 * Uold[0, 2:-2] - 5/3 * Uold[1, 2:-2] + 0.5 * Uold[2, 2:-2] + 1/3 * Uold[3, 2:-2] - 1/12 * Uold[4, 2:-2]) 
            + ly * (-1/12 * Uold[1, :-4] + 4/3 * Uold[1, 1:-3] - 2.5 * Uold[1, 2:-2] + 4/3 * Uold[1, 3:-1] - 1/12 * Uold[1, 4:])
            + dt * phi(Uold[1, 2:-2], X[1, 2:-2], Y[1, 2:-2])
        )
        
        Uh[-2, 2:-2] = (
            Uold[-2, 2:-2]+
            lx * (-1/12 * Uold[-5, 2:-2] + 1/3 * Uold[-4, 2:-2] + 0.5 * Uold[-3, 2:-2] - 5/3 * Uold[-2, 2:-2] + 11/12 * Uold[-1, 2:-2]) 
            + ly * (-1/12 * Uold[-2, :-4] + 4/3 * Uold[-2, 1:-3] - 2.5 * Uold[-2, 2:-2] + 4/3 * Uold[-2, 3:-1] - 1/12 * Uold[-2, 4:])
            + dt * phi(Uold[-2, 2:-2], X[-2, 2:-2], Y[-2, 2:-2])
        )
        Uh[2:-2, 1] = (
            Uold[2:-2, 1]+
            lx * (-1/12 * Uold[:-4, 1] + 4/3 * Uold[1:-3, 1] - 2.5 * Uold[2:-2, 1] + 4/3 * Uold[3:-1, 1] - 1/12 * Uold[4:, 1])
            + ly * (11/12 * Uold[2:-2, 0] - 5/3 * Uold[2:-2, 1] + 0.5 * Uold[2:-2, 2] + 1/3 * Uold[2:-2, 3] - 1/12 * Uold[2:-2, 4]) 
            + dt * phi(Uold[2:-2, 1], X[2:-2, 1], Y[2:-2, 1])
        )
        Uh[2:-2, -2] = (
            Uold[2:-2, -2]+
            lx * (-1/12 * Uold[:-4, -2] + 4/3 * Uold[1:-3, -2] - 2.5 * Uold[2:-2, -2] + 4/3 * Uold[3:-1, -2] - 1/12 * Uold[4:, -2])
            + ly * (-1/12 * Uold[2:-2, -5] + 1/3 * Uold[2:-2, -4] + 0.5 * Uold[2:-2, -3] - 5/3 * Uold[2:-2, -2] + 11/12 * Uold[2:-2, -1]) 
            + dt * phi(Uold[2:-2, -2], X[2:-2, -2], Y[2:-2, -2])
        )


        # 4 coins internes
        Uh[1,1] = (
            Uold[1,1]+
            lx *(11/12*Uold[0,1] - 5/3*Uold[1,1] +0.5*Uold[2,1]+1/3*Uold[3,1]-1/12*Uold[4,1])
            + ly * (11/12*Uold[1,0] - 5/3*Uold[1,1] +0.5*Uold[1,2]+1/3*Uold[1,3]-1/12*Uold[1,4])
            + dt * phi(Uold[1,1], X[1,1], Y[1,1])
        )
        Uh[-2,1] = (
            Uold[-2,1]+
            lx *(-1/12*Uold[-5,1] +1/3*Uold[-4,1] +0.5*Uold[-3,1]-5/3*Uold[-2,1]+11/12*Uold[-1,1])
            + ly * (11/12*Uold[-2,0] - 5/3*Uold[-2,1] +0.5*Uold[-2,2]+1/3*Uold[-2,3]-1/12*Uold[-2,4])
            + dt * phi(Uold[-2,1], X[-2,1], Y[-2,1])
        )
        Uh[1,-2] = (
            Uold[1, -2]+
            lx *(11/12*Uold[0,-2] - 5/3*Uold[1,-2] +0.5*Uold[2,-2]+1/3*Uold[3,-2]-1/12*Uold[4,-2])
            + ly * (-1/12*Uold[1,-5] +1/3*Uold[1,-4] +0.5*Uold[1,-3]-5/3*Uold[1,-2]+11/12*Uold[1,-1])
            + dt * phi(Uold[1,-2], X[1,-2], Y[1,-2])
        )
        Uh[-2,-2] = (
            Uold[-2, -2]+
            lx *(-1/12*Uold[-5,-2] +1/3*Uold[-4,-2] +0.5*Uold[-3,-2]-5/3*Uold[-2,-2]+11/12*Uold[-1,-2])
            + ly * (-1/12*Uold[-2,-5] +1/3*Uold[-2,-4] +0.5*Uold[-3,-2]-5/3*Uold[-2,-2]+11/12*Uold[-2,-1])
            + dt * phi(Uold[-2,-2], X[-2,-2], Y[-2,-2])
        )

        
        # Apply boundary conditions without corners (order = 4)
        Uh[0, 1:-1] = 48/25 * Uold[1, 1:-1] - 36/25 * Uold[2, 1:-1] + 48/75*Uold[3,1:-1] - 12/100*Uold[4,1:-1]
        Uh[-1, 1:-1] = -12/100 * Uold[-5, 1:-1] +48/75* Uold[-4, 1:-1] - 36/25*Uold[-3,1:-1] + 48/25*Uold[-2,1:-1]
        Uh[1:-1, 0] = 48/25 * Uold[1:-1, 1] - 36/25 * Uold[1:-1, 2] + 48/75*Uold[1:-1,3] - 12/100*Uold[1:-1,4]
        Uh[1:-1, -1] = -12/100 * Uold[1:-1, -1] +48/75* Uold[1:-1,-4] - 36/25*Uold[1:-1,-3] + 48/25*Uold[1:-1,-2]
        
        
        # Calculer les coins (order = 4)
        Uh[0, 0] = (48/25 * Uold[0,1] - 36/25 * Uold[0, 2] + 48/75*Uold[0,3] - 12/100*Uold[0,4] + 48/25 * Uold[1,0] - 36/25 * Uold[2,0] + 48/75*Uold[3,0] - 12/100*Uold[4,0])/2
        Uh[-1,0] = (48/25 * Uold[-2,0] - 36/25 * Uold[-3, 0] + 48/75*Uold[-4,0] - 12/100*Uold[-5,0] + 48/25 * Uold[-1,-2] - 36/25 * Uold[-1,-3] + 48/75*Uold[-1,-4] - 12/100*Uold[-1,-5])/2
        Uh[0,-1] = (48/25 * Uold[0,-2] - 36/25 * Uold[0, -3] + 48/75*Uold[0,-4] - 12/100*Uold[0,-5] + 48/25 * Uold[1,-1] - 36/25 * Uold[2,-1] + 48/75*Uold[3,-1] - 12/100*Uold[4,-1])/2
        Uh[-1,-1] =(48/25 * Uold[-1,-2] - 36/25 * Uold[-1, -3] + 48/75*Uold[-1,-4] - 12/100*Uold[-1,-5] + 48/25 * Uold[-2,-1] - 36/25 * Uold[-3,-1] + 48/75*Uold[-4,-1] - 12/100*Uold[-5,-1])/2
        
        

        # Remettre la fenetre dans Uh
        Uh = fenetre(Uh,X,Y)
    
        # Store Nt_print_max iterations
        if it % ((T//dt)//Nt_print_max) == 0:
            Uh_history.append((t, Uh.copy()))
        
    #Save la solution au temps final T
    Uh_history.append((t, Uh.copy())) 
    
    return Uh, Uh_history



# Run the simulation
T = 2
D = 1  # Thermal diffusivity of air in m^2/s
mesh_dimensions = (30,30)
CFL = 0.25
final_temperature_distribution, Uh_history = schema_chaleur2D_explicite_o4(
    mesh_dimensions, T=T, D=D, CFL=CFL, Nt_print_max=30
)

# Generate the grid for plotting
m, p = mesh_dimensions
x = np.linspace(0, 1, m)
y = np.linspace(0, 1, p)
X, Y = np.meshgrid(x, y)

# Plot the progression of temperature distributions with interactive controls
plot_progression_with_controls(Uh_history, X, Y, plot_type='3d')
# %%
