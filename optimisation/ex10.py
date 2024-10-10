#%%
import numpy as np
import matplotlib.pyplot as plt

#%%

import numpy as np
from scipy.optimize import fsolve

# Définir le système d'équations non linéaires
def system(vars):
    x, y, z = vars
    f1 = 3*x**2*y + 3*z*x**2  # Première équation
    f2 = x**3 - z             # Deuxième équation
    f3 = x**3 - y - 1         # Troisième équation
    return [f1, f2, f3]

# Guess initial pour la solution (il est important d'avoir une estimation initiale)
initial_guess = [1, 1, 1]  # Estimation initiale pour x, y, z

# Résolution du système avec fsolve
solution = fsolve(system, initial_guess)

# Affichage de la solution
print("Solution (x, y, lambda):", solution)

# Vérification de la solution
print(3*solution[0]**2*solution[1] + 3*solution[2]*solution[0]**2)
print(solution[0]**3 - solution[2])
print(solution[0]**3-solution[1]-1)



# %%
