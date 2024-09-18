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





#%%
# n = 100

n = 100
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
        print(grad[0],grad[-1])
        x = x - learning_rate * grad  # Mise à jour de x en fonction du gradient
        history.append(x)  # Ajouter le nouveau point à l'historique

        # Afficher les informations sur l'avancement
        #print(f"Iteration {i+1}: cost = {cost_function(x, y)}")

    return x, history

# Exemple d'utilisation
# Dimension du vecteur
starting_point = x0  # Point de départ aléatoire  # Vecteur y fixé (dimension n = 100)
learning_rate = 0.01  # Taux d'apprentissage
num_iterations = 500  # Nombre d'itérations

# Lancer la descente de gradient
solution, history = gradient_descent(starting_point, y, learning_rate, num_iterations)


#print("Solution finale:", solution)
#print(gradient(x0,y))


# %%
