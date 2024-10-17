#%%

#  L = J + <lambda,E>
# Grad(L) = 0 <=> Grad(J) + lambda*Grad(E) = 0

import numpy as np
from scipy.optimize import fsolve, root 

# Définir le système d'équations non linéaires
def system(vars):
    x, y, z = vars
    f1 = 3*x**2*y + 3*z*x**2  # Première équation
    f2 = x**3 - z             # Deuxième équation
    f3 = x**3 - y - 1         # Troisième équation
    return [f1, f2, f3]

V = 1000
S = 10

def fun(x):
    return [x[1] + x[2] + x[3]*x[2]*x[1] + x[4]*x[1],       #dL/dx1
            x[0] + x[2] + x[3]*x[0]*x[2] + x[4]*x[0],       #dL/dx2
            x[0] + x[1] + x[3]*x[0]*x[1] + 0,               #dL/dx3
            x[0]*x[1]*x[2] - V + eps,                       #dL/dp1 : contrainte C1=0
            x[0]*x[1] - S  + eps                            #dL/dp2 : contrainte C2=0
            ]

# Guess initial pour la solution (il est important d'avoir une estimation initiale)
initial_guess = [1]*5  # Estimation initiale pour x, y, z, lambda1, lambda2

# Résolution du système avec fsolve
eps = 0
solution = root(fun, initial_guess)

# Affichage de la solution
x_opt = [solution.x[0],solution.x[1],solution.x[2]]
print("Solution (x, y, z):", x_opt)
print("Solution lambda1, lambda2:", solution.x[3], solution.x[4])


eps = 1e-3
solution_eps = root(fun, initial_guess)
x_opt_eps = [solution_eps.x[0],solution_eps.x[1],solution_eps.x[2]]


def J(v):
    x,y,z = v
    return x*y + x*z + y*z


print("dJ/dC1 = -lambda1 = ",(J(x_opt_eps)-J(x_opt))/eps)



# %%
