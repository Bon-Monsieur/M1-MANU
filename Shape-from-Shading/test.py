import numpy as np
import scipy.sparse as sp
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

matplotlib.use("TkAgg")  # or 'Qt5Agg' if you prefer Qt

# Merci Ronan pour l'optimisation :D

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

    if fig == "pwfe":
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
    
    if fig == "x2_0bd":
        ax0 = int((Nx-1)/2)
        for j in range(Nx):
            Un[j,ax0] = 0
        return Un
    
    if fig == "x2_mixed_bd":
        ax0 = int((Nx-1)/2)
        for j in range(Nx):
            Un[j,ax0] = 0
        return Un
    
    if fig == "vase":
        x_vals = np.linspace(-0.5, 0.5, Nx)
        y_vals = np.linspace(-0.5, 0.5, Ny)
        X,Y = np.meshgrid(x_vals, y_vals)
        I = lambda x, y: np.where(
            np.isnan(dvase_dx(x, y)) & np.isnan(dvase_dy(x, y)), 1,
            1 / np.sqrt(1 + dvase_dx(x, y)**2 + dvase_dy(x, y)**2)
        )
        mask = (I(x_vals, y_vals) == 1 ) & (g(X)**2 - Y**2 > 0)
        Un[mask] = (np.sqrt(g(X)**2 - Y**2))[mask]  # Donne la vraie valeur du vase aux points critiques

        return Un



def erreur(Un, Nx, Ny, fig, x, y):
    x = np.linspace(0, 1, Nx)
    y = np.linspace(0, 1, Ny)

    if fig == "parabola":
        sol_exacte = lambda x, y: 16 * (y * (1 - y) * x * (1 - x))

    elif fig == "reverse_parabola":
        sol_exacte = lambda x, y: -16 * (y * (1 - y) * x * (1 - x))

    elif fig == "pwfe":
        sol_exacte = lambda x, y: -16 * (y * (1 - y) * x * (1 - x))

    elif fig == "pyramid":
        sol_exacte = lambda x, y: 1 - 2 * np.maximum(np.abs(0.5 - x), np.abs(0.5 - y))

    elif fig in ["fig7", "fig8"]:
        sol_exacte = lambda x, y: np.sin(2 * np.pi * x) * np.sin(2 * np.pi * y)
        
    elif fig=="x2_0bd":
        x = np.linspace(-1, 1, Nx)
        y = np.linspace(-1, 1, Ny)
        return 1000
        
    elif fig=="x2_mixed_bd":
        x = np.linspace(-1, 1, Nx)
        y = np.linspace(-1, 1, Ny)
        sol_exacte = lambda x, y: np.where(x**2 >= 0, x**2, 0)

    elif fig=="vase":
        x = np.linspace(-0.5, 0.5, Nx)
        y = np.linspace(-0.5, 0.5, Ny)
        sol_exacte = lambda x, y: np.sqrt(np.maximum(g(x)**2 - y**2, 0))
    
    X, Y = np.meshgrid(x, y)

    return np.mean(np.abs(Un - sol_exacte(X, Y)))



# Methode du point fixe pour le probleme de SFS
def SFS_fixed_point_method(Nx, Ny, fig="parabola",epsilon=1e-4,maxiter=2000):

    # Maillage par défaut
    x = np.linspace(0, 1, Nx)
    y = np.linspace(0, 1, Ny)

    # Initialisation 
    Un = np.full((Nx, Ny), 0.0)  # U0 == 0

    # Fonction de l'intensité lumineuse en fonction de la figure demandée et définition des bonnes bornes du maillage pour un bel affichage
    if fig == "parabola":
        I = (
            lambda x, y: 1/np.sqrt(1+(16 * y * (1 - y) * (1 - 2 * x))**2
            + (16 * x * (1 - x) * (1 - 2 * y))**2)
        )
    elif fig == "reverse_parabola":
        I = (
            lambda x, y: 1/np.sqrt(1+(16*y*(1-y)*(1-2*x))**2
            + (16*x*(1-x)*(1-2*y))**2)
        )
    elif fig == "pyramid":
        I = (
            lambda x, y: np.ones_like(X) / np.sqrt(5)
        )
    elif fig == "pwfe":
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
    elif fig == "x2_0bd":
        x = np.linspace(-1, 1, Nx)
        y = np.linspace(-1, 1, Ny)
        I = (
            lambda x, y: 1/np.sqrt(1+(2*x)**2)
        )
    elif fig == "x2_mixed_bd":
        x = np.linspace(-1, 1, Nx)
        y = np.linspace(-1, 1, Ny)
        I = (
            lambda x, y: 1/np.sqrt(1+(2*x)**2)
        )
        # Conditions aux bords
        Un[:,0] = Un[:,-1] = 1
        Un[0,:] = Un[-1,:] = x**2
    elif fig == "vase":
        x = np.linspace(-0.5, 0.5, Nx)
        y = np.linspace(-0.5, 0.5, Ny)
        I = lambda x, y: np.where(
            np.isnan(dvase_dx(x, y)) & np.isnan(dvase_dy(x, y)), 1,
            1 / np.sqrt(1 + dvase_dx(x, y)**2 + dvase_dy(x, y)**2)
        )
        # Condition aux bords
        Un[:,0]  = np.sqrt(np.maximum(g(-0.5)**2 - y**2, 0))
        Un[:,-1] = np.sqrt(np.maximum(g(0.5)**2 - y**2, 0))
        
        

    # Def maillage et pas
    X, Y = np.meshgrid(x, y)
    Dx = x[1] - x[0]
    Dy = y[1] - y[0]
    Dt = Dx * Dy / np.sqrt(Dx**2 + Dy**2)


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
   
    # Methode du pt fixe
    for k in range(maxiter+1):
        if(erreur(Un,Nx,Ny,fig,x,y)<=epsilon):
            break
        Un = cond(
            Un, Nx, Ny, fig      # Applique les conditions pour les endroits sur la frontière
        ) 
        Un[1:-1, 1:-1] = Un[1:-1, 1:-1] - Dt * G(Un)[1:-1, 1:-1]  
        
    # Corrige les imperfections de la solution pour l'affichage du vase
    if fig=="vase":
        Un = cond(Un,Nx,Ny,fig)

    erreur_globale = erreur(Un, Nx, Ny, fig, x, y)  # Calcul de l'erreur

    # ======== AFFICHAGE ======= #

    figure = plt.figure(figsize=(10, 4))
    ax = figure.add_subplot(1, 2, 1)

    # Calcul des valeurs de I sur le maillage
    Z = I(X,Y)
    
    # Premier graphique
    contour1 = ax.contourf(
        X, Y, Z, levels=np.linspace(0, 1, 51), cmap="viridis", vmin=0, vmax=1
    )
    cbar = figure.colorbar(contour1, ax=ax, label="I(v)")
    cbar.set_ticks(np.linspace(0, 1, 6))
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Intensité lumineuse")

    # Deuxième figure
    ax = figure.add_subplot(1, 2, 2, projection="3d")
    ax.plot_wireframe(X, Y, Un, color="black", linewidth=1)
    #surf = ax.plot_surface(X, Y, Un, color="white", edgecolor="black", linewidth=0.1, shade=False)
    surf = ax.plot_surface(X, Y, Un, color="white", alpha=1)
    ax.view_init(elev=15, azim=-135)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    if fig=="vase":
        ax.set_zlim(0, 0.7)
    ax.set_title("Shape reconstructed from the intensity")

    #print(erreur_globale)
    ax.text2D(0., -0.1, f"Erreur: ${erreur_globale:.2e}$", transform=ax.transAxes)
    ax.text2D(0.6, -0.1, f"Nb_itération: ${k:.2f}$", transform=ax.transAxes)

    plt.show()


# ====== Fonctions pour le vase ====== #

g = lambda x: 0.15 - 0.025 * (6*x - 1) * (2*x - 1)**2 * (3*x + 2)**2 * (2*x + 1)
dg_dx = lambda x, dx=1e-5: (g(x + dx) - g(x - dx)) / (2 * dx)

# Dérivées partielles dz/dx et dz/dy sous forme lambda
dvase_dx = lambda x, y: np.where(g(x)**2 - y**2 > 0, (g(x) * dg_dx(x)) / np.sqrt(g(x)**2 - y**2), 0)
dvase_dy = lambda x, y: np.where(g(x)**2 -y**2 > 0, -y / np.sqrt(g(x)**2 - y**2), 0)


#======  UTILISATION  ======#

SFS_fixed_point_method(Nx=101, Ny=101, fig="vase",epsilon=1e-4,maxiter=4000)