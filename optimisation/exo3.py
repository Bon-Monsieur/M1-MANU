#%%
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython
get_ipython().run_line_magic("matplotlib", "widget")
from pylab import cm
#%%
# n = 2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Définir la fonction f(x)
def f(x1, x2, y):
    x = np.array([x1, x2])  # Créer le vecteur x = (x1, x2)
    return (x1 * y[0] + x2 * y[1]) * np.exp(-(x1**2 + x2**2))  # f(x) = <x, y> * exp(-||x||²)

# Fixer un vecteur y
y = np.array([1, 1])  # Par exemple, y = (1, 1)

# Créer une grille de valeurs pour x1 et x2
x1 = np.linspace(-2, 2, 100)
x2 = np.linspace(-2, 2, 100)
X1, X2 = np.meshgrid(x1, x2)

# Calculer les valeurs de z = f(x1, x2, y)
Z = f(X1, X2, y)

# Créer un graphique 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Tracer la surface
ax.plot_surface(X1, X2, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
# Ajouter des labels
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('f(x1, x2)')

# Afficher le graphique
plt.show() 



#############   descente de gradient    ##################

n = 2
x0 = np.array([1]*n)
y = np.array([i for i in range(1,n+1)])

# Fonctionnelle f(x) = <x, y> * exp(-||x||^2)
def cost_function(x, y):
    return np.dot(x, y) * np.exp(-np.linalg.norm(x)**2)

# Gradient de la fonctionnelle
def gradient(x, y):
    # Calcul du gradient de f(x)
    term1 = y * np.exp(-np.linalg.norm(x)**2)
    term2 = -2 * x * np.dot(x, y) * np.exp(-np.linalg.norm(x)**2)
    return term1 + term2

# Méthode de descente de gradient
def gradient_descent(starting_point, y, learning_rate=0.1, num_iterations=1000):
    x = starting_point  # Initialiser x au point de départ
    history = [x]  # Stocker les positions pour observer l'évolution

    for i in range(num_iterations):
        grad = gradient(x, y)  # Calculer le gradient au point courant
        x = x - learning_rate * grad  # Mise à jour de x en fonction du gradient
        history.append(x)  # Ajouter le nouveau point à l'historique

        # Afficher les informations sur l'avancement
        #print(f"Iteration {i+1}: cost = {cost_function(x, y)}")

    return x, history

# Exemple d'utilisation
# Dimension du vecteur
starting_point = x0  # Point de départ aléatoire  # Vecteur y fixé (dimension n = 100)
learning_rate = 0.01  # Taux d'apprentissage
num_iterations = 5000  # Nombre d'itérations

# Lancer la descente de gradient
solution, history = gradient_descent(starting_point, y, learning_rate, num_iterations)

print("Solution finale:", solution)


# %%
# Utiliser les différences finies pour calculer le gradient 

import numpy as np

# Fonctionnelle f(x) = <x, y> * exp(-||x||^2)
def cost_function(x, y):
    return np.dot(x, y) * np.exp(-np.linalg.norm(x)**2)

# Gradient de la fonctionnelle utilisant les différences finies
def finite_difference_gradient(x, y, h=1e-5):
    n = len(x)
    grad = np.zeros(n)  # Initialiser le gradient à un vecteur nul
    fx = cost_function(x, y)  # Calculer la valeur actuelle de f(x)
    
    for i in range(n):
        # Créer un vecteur perturbé x + h * e_i
        x_step = np.copy(x)
        x_step[i] += h
        
        # Calculer la différence finie pour la dérivée partielle
        grad[i] = (cost_function(x_step, y) - fx) / h
    
    return grad

# Méthode de descente de gradient
def gradient_descent(starting_point, y, learning_rate=0.1, num_iterations=1000):
    x = starting_point  # Initialiser x au point de départ
    history = [x]  # Stocker les positions pour observer l'évolution

    for i in range(num_iterations):
        grad = finite_difference_gradient(x, y)  # Calculer le gradient via différences finies
        x = x - learning_rate * grad  # Mise à jour de x en fonction du gradient
        history.append(np.copy(x))  # Ajouter le nouveau point à l'historique

    return x, history

# Exemple d'utilisation
n = 2  # Dimension du vecteur
x0 = np.array([1]*n)  # Point de départ
y = np.array([i for i in range(1, n+1)])  # Vecteur y fixé

learning_rate = 0.01  # Taux d'apprentissage
num_iterations = 5000  # Nombre d'itérations

# Lancer la descente de gradient
solution, history = gradient_descent(x0, y, learning_rate, num_iterations)

print("Solution finale:", solution)





# %%
import numpy as np
import matplotlib.pyplot as plt

# Fonctionnelle f(x) = <x, y> * exp(-||x||^2)
def cost_function(x, y):
    return np.dot(x, y) * np.exp(-np.linalg.norm(x)**2)

# Gradient de la fonctionnelle (gradient explicite)
def gradient(x, y):
    term1 = y * np.exp(-np.linalg.norm(x)**2)
    term2 = -2 * x * np.dot(x, y) * np.exp(-np.linalg.norm(x)**2)
    return term1 + term2

# Gradient approximé avec les différences finies
def finite_difference_gradient(x, y, h=1e-5):
    n = len(x)
    grad_approx = np.zeros(n)
    fx = cost_function(x, y)
    
    for i in range(n):
        x_step = np.copy(x)
        x_step[i] += h
        grad_approx[i] = (cost_function(x_step, y) - fx) / h
    
    return grad_approx

# Fonction pour calculer la différence entre les deux gradients
def gradient_difference_norm(x, y, h_values):
    grad_exact = gradient(x, y)
    differences = []
    
    for h in h_values:
        grad_approx = finite_difference_gradient(x, y, h)
        diff = np.linalg.norm(grad_exact - grad_approx)
        differences.append(diff)
    
    return differences

# Exemple d'utilisation
n = 2  # Dimension du vecteur
x0 = np.array([1]*n)  # Point de départ
y = np.array([i for i in range(1, n+1)])  # Vecteur y fixé

# Valeurs de h à tester, plus concentrées
h_values = np.logspace(-5, -1, 50)  # h de 10^-5 à 10^-1

# Calculer la différence entre le gradient exact et l'approximation
differences = gradient_difference_norm(x0, y, h_values)

# Tracer le graphe
plt.figure(figsize=(8, 6))
plt.plot(h_values, differences, marker='o', linestyle='-', color='b', label='Différence entre gradients')
plt.xscale('log')  # Échelle logarithmique pour h
plt.yscale('log')  # Échelle logarithmique pour les différences
plt.xlabel('h')
plt.ylabel('Norme de la différence entre gradients')
plt.title('Différence entre le gradient exact et le gradient approximé par différences finies')
plt.grid(True)
plt.legend(loc='upper left')
plt.show()

# %%
