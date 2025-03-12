import numpy as np
import scipy.sparse as sp
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use("TkAgg")  # or 'Qt5Agg' if you prefer Qt


# Fonction qui permet de forcer la valeur de mon estimation aux points critiques de ma forme
def cond(Un, Nx, Ny, fig="parabola"):
    if fig == "parabola":
        ax = int((Nx - 1) / 2)
        ay = int((Ny - 1) / 2)
        Un[ax, ay] = 1  # modifie uniquement le centre de la parabole
        return Un

    if fig == "reverse_parabola":
        ax = int((Nx - 1) / 2)
        ay = int((Ny - 1) / 2)
        Un[ax, ay] = -1  # modifie uniquement le centre de la parabole
        return Un

    if fig == "pyramid":
        return Un

    if fig == "parabola_with_forced_elevation":
        ax = int((Nx - 1) / 2)
        ay = int((Ny - 1) / 2)
        Un[ax, ay] = 47 / 81  # modifie uniquement le centre de la parabole
        return Un

    if fig == "fig7":
        ax = int((Nx - 1) / 2)  # moitié du maillage
        ay = int((Ny - 1) / 2)  # moitié du maillage
        Un[ax, ay] = 0
        bx = int(ax / 2)  # quart du maillage
        by = int(ay / 2)  # quart du maillage
        cx = 3 * bx
        cy = 3 * by
        Un[bx, by] = Un[cx, cy] = 1
        Un[bx, cy] = Un[cx, by] = -1
        return Un
    if fig == "fig8":
        ax = int((Nx - 1) / 2)  # moitié du maillage
        ay = int((Ny - 1) / 2)  # moitié du maillage
        Un[ax, ay] = 2
        bx = int(ax / 2)  # quart du maillage
        by = int(ay / 2)  # quart du maillage
        cx = 3 * bx
        cy = 3 * by
        Un[bx, by] = Un[cx, cy] = Un[bx, cy] = Un[cx, by] = 1
        return Un
    if fig == "test":
        return Un



def erreur(Un, Nx, Ny, fig, x, y):
    x = np.linspace(0, 1, Nx)
    y = np.linspace(0, 1, Ny)

    X, Y = np.meshgrid(x, y)

    if fig == "parabola":
        sol_exacte = lambda x, y: 16 * (y * (1 - y) * x * (1 - x))
    elif fig == "reverse_parabola":
        sol_exacte = lambda x, y: -16 * (y * (1 - y) * x * (1 - x))
    elif fig == "parabola_with_forced_elevation":
        sol_exacte = lambda x, y: -16 * (y * (1 - y) * x * (1 - x))
    elif fig == "pyramid":
        sol_exacte = lambda x, y: 1 - 2 * np.maximum(np.abs(0.5 - x), np.abs(0.5 - y))
    elif fig in ["fig7", "fig8"]:
        sol_exacte = lambda x, y: np.sin(2 * np.pi * x) * np.sin(2 * np.pi * y)
    elif fig=="test":
        sol_exacte = lambda x, y: np.sqrt(1 - np.maximum(np.abs(x - 0.5), np.abs(y - 0.5)))
    return np.mean(np.abs(Un - sol_exacte(X, Y)))




# Methode du point fixe pour le probleme de SFS
def SFS_fixed_point_method(Nx, Ny, fig="parabola",epsilon=1e-4,maxiter=2000):

    # Définition du maillage
    x = np.linspace(0, 1, Nx)
    y = np.linspace(0, 1, Ny)

    X, Y = np.meshgrid(x, y)
    Dx = x[1] - x[0]
    Dy = y[1] - y[0]
    Dt = Dx * Dy / np.sqrt(Dx**2 + Dy**2)

    # Fonction de l'intensité lumineuse en fonction de la figure demandée
    if fig == "parabola":
        I = (
            lambda x, y: 1/np.sqrt(1+(16 * y * (1 - y) * (1 - 2 * x))**2
            + (16 * x * (1 - x) * (1 - 2 * y))**2)
        )

    if fig == "reverse_parabola":
        I = (
            lambda x, y: 1/np.sqrt(1+(16*y*(1-y)*(1-2*x))**2
            + (16*x*(1-x)*(1-2*y))**2)
        )
    elif fig == "pyramid":
        I = lambda x, y: np.ones_like(X) / np.sqrt(5)
    elif fig == "parabola_with_forced_elevation":
        I = (
            lambda x, y: 1/np.sqrt(1+(16 * y * (1 - y) * (1 - 2 * x)) ** 2
            + (16 * x * (1 - x) * (1 - 2 * y)) ** 2)
        )
    elif fig == "fig7":
        I = (
            lambda x, y: 1/np.sqrt(1+(2 * np.pi * np.sin(2 * np.pi * y) * np.cos(2 * np.pi * x))
            ** 2
            + (2 * np.pi * np.sin(2 * np.pi * x) * np.cos(2 * np.pi * y)) ** 2)
        )
    elif fig == "fig8":
        I = (
            lambda x, y: 1/np.sqrt(1+(2 * np.pi * np.sin(2 * np.pi * y) * np.cos(2 * np.pi * x))
            ** 2
            + (2 * np.pi * np.sin(2 * np.pi * x) * np.cos(2 * np.pi * y)) ** 2)
        )
    elif fig == "test":
        I = lambda x, y: np.ones_like(X)*0.01

    # Définition de la normale pour le SFS
    n = lambda x, y: np.sqrt(1/I(x, y)**2-1)

    ## Building Finite Differences Operators
    # forward on x, backwards on x, forward on y, backwards on y
    Dxp = sp.diags_array([-1, 1], offsets=[0, 1], shape=(Nx, Nx)) / Dx
    Dxm = sp.diags_array([-1, 1], offsets=[-1, 0], shape=(Nx, Nx)) / Dx
    Dyp = sp.diags_array([-1, 1], offsets=[0, 1], shape=(Ny, Ny)) / Dy
    Dym = sp.diags_array([-1, 1], offsets=[-1, 0], shape=(Ny, Ny)) / Dy

    # injected into 2D by tensor product (with flattened matrix)
    DDxp = sp.kron(sp.eye_array(Ny), Dxp)
    DDxm = sp.kron(sp.eye_array(Ny), Dxm)
    DDyp = sp.kron(Dyp, sp.eye_array(Nx))
    DDym = sp.kron(Dym, sp.eye_array(Nx))
    # We now have 2D FD operators

    # Les deux fonctions g et G du papier
    def G(U):
        fU = U.flatten()
        R = np.sqrt(
            np.maximum(np.maximum(DDxm @ fU, 0.0), np.maximum(-DDxp @ fU, 0.0)) ** 2
            + np.maximum(np.maximum(DDym @ fU, 0.0), np.maximum(-DDyp @ fU, 0.0)) ** 2
        ).reshape(Nx, Ny) - n(X, Y)
        return R

    # Initialisation de mon itération
    Un = np.full((Nx, Ny), 0.0)  # U0 == 0

    # Boucle itérative à modifier en while pour forcer la convergence en fonction d'un epsilon donné
    # Ici on fait 200 itérations, mais on peut demander plus (attention à la lenteur du code)
    
    for k in range(maxiter+1):
        if(erreur(Un,Nx,Ny,fig,x,y)<=epsilon):
            break
        Un = cond(
            Un, Nx, Ny, fig
        )  # Applique les conditions pour les endroits où I(x)=1
        Un[1:-1, 1:-1] = Un[1:-1, 1:-1] - Dt * G(Un)[1:-1, 1:-1]  # methode du pt fixe
        
    # Up1 = cond(Up1,nb_pt,fig)
    erreur_globale = erreur(Un, Nx, Ny, fig, x, y)  # Calcul de l'erreur

    # ======== AFFICHAGE ======= #

    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 2, 1)

    # Calcul des valeurs de I sur le maillage
    Z = I(X, Y)
    
    # Premier graphique
    contour1 = ax.contourf(
        X, Y, Z, levels=np.linspace(0, 1, 51), cmap="viridis", vmin=0, vmax=1
    )
    cbar = fig.colorbar(contour1, ax=ax, label="I(v)")
    cbar.set_ticks(np.linspace(0, 1, 5))
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Intensité lumineuse")

    # Deuxième figure
    ax = fig.add_subplot(1, 2, 2, projection="3d")
    ax.plot_wireframe(X, Y, Un, color="black", linewidth=1)
    surf = ax.plot_surface(X, Y, Un, color="white", alpha=1)
    ax.view_init(elev=15, azim=-135)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Shape reconstructed from the intensity")

    print(erreur_globale)
    ax.text2D(0., -0.1, f"Erreur: ${erreur_globale:.2e}$", transform=ax.transAxes)
    ax.text2D(0.6, -0.1, f"Nb_itération: ${k:.2f}$", transform=ax.transAxes)

    plt.show()


"""
======= Utilisation =======
Il est possible de consulter 5 résultats différents de Shape-From-Shading
Pour utiliser le code il suffit d'appeler la fonction SFS_fixed_point_method avec deux arguments:
    - le nombre de points du maillage 
    - La forme que l'on souhaite reconstruire

Il est recommandé d'utiliser un nombre de point impair afin d'avoir une belle symétrie des résultats 
Il est possible de donner les formes suivantes comme argument (sous la forme de chaîne de caractère):
    - "parabola"
    - "reverse_parabola"
    - "pyramid"
    - "parabola_with_forced_elevation"
    - "fig8"

Exemple d'appel:    SFS_fixed_point_method(nb_pt=21,fig="parabola")
"""


SFS_fixed_point_method(Nx=101, Ny=101, fig="test",epsilon=1e-5,maxiter=2000)
