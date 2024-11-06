# %%
import numpy as np
import matplotlib.pyplot as plt

def uzawa_algorithm(x0, p0, rho, num_iterations=1000):
    """
    Algorithme d'Uzawa pour minimiser la fonctionnelle J(x1, x2) sous la contrainte x1 + x2 = 1.
    
    Paramètres:
        x0 (ndarray): Point de départ pour les variables de décision (x1, x2).
        p0 (float): Point de départ pour le multiplicateur de Lagrange.
        rho (float): Paramètre de mise à jour pour le multiplicateur de Lagrange.
        num_iterations (int): Nombre d'itérations pour la convergence.
        
    Retourne:
        x (ndarray): Solution optimale pour (x1, x2).
        p (float): Valeur optimale du multiplicateur de Lagrange.
    """
    
    # Initialisation
    x = np.array(x0)
    p = p0
    save_x = [x]
    save_p = [p]

    for _ in range(num_iterations):
        # Mise à jour de x en minimisant le Lagrangien L(x, p)
        x1, x2 = x
        grad_x1 = 2 * x1 + 2 + p            # Gradient par rapport à x1
        grad_x2 = 4 * x2 + 3 + p            # Gradient par rapport à x2
        
        x1_new = x1 - rho * grad_x1
        x2_new = x2 - rho * grad_x2
        x = np.array([x1_new, x2_new])

     
        
        # Mise à jour de p (multiplicateur de Lagrange)
        constraint_violation = x1_new + x2_new - 1
        p = p + rho * constraint_violation

        save_x.append(x)
        save_p.append(p)

    return save_x, save_p

# Paramètres d'initialisation
x0 = [0, 0]     # Point de départ pour (x1, x2)
p0 = 0.1        # Point de départ pour le multiplicateur de Lagrange p
rho = 0.1      # Paramètre de mise à jour

# Exécution de l'algorithme
save_x, save_p = uzawa_algorithm(x0, p0, rho)
print("Solution optimale x:", save_x[-1])
print("Multiplicateur de Lagrange optimal p:", save_p[-1])

plt.plot(save_x)
plt.plot(save_p)


A = np.array([[1,0],[0,2]])


# %%
