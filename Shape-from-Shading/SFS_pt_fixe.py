import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

# Fonction qui permet de forcer la valeur de mon estimation aux points critiques de ma forme
def cond(Un,nb_pt,fig="parabola"):
    if fig=="parabola":
        a = int((nb_pt-1)/2)
        Un[a,a] = 1   # modifie uniquement le centre de la parabole
        return Un

    if fig == "reverse_parabola":
        a = int((nb_pt-1)/2)
        Un[a,a] = -1   # modifie uniquement le centre de la parabole
        return Un

    if fig == "pyramid":
        return Un
    
    if fig == "parabola_with_forced_elevation":
        a = int((nb_pt-1)/2)
        Un[a,a] = 47/81  # modifie uniquement le centre de la parabole
        return Un

    if fig == "fig7":
        a = int((nb_pt-1)/2) # moitié du maillage
        Un[a,a] = 0
        b = int(a/2)  # quart du maillage
        c = 3*b
        Un[b,b]=Un[c,c]=1
        Un[b,c]=Un[c,b]=-1
        return Un
    if fig == "fig8":
        a = int((nb_pt-1)/2) # moitié du maillage
        Un[a,a] = 2
        b = int(a/2)  # quart du maillage
        c = 3*b
        Un[b,b]=Un[c,c]=Un[b,c]=Un[c,b]=1
        return Un
    if fig == "test":
        for j in range(nb_pt):
            Un[int((nb_pt-1)/2),j] = 0
        return Un

def erreur(Un,nb_pt,fig,x,y):
    res = 0
    count = 0

    if fig=="parabola":
        sol_exacte = lambda v: 16*(v[1]*(1-v[1])*v[0]*(1-v[0]))
    if fig=="reverse_parabola":
        sol_exacte = lambda v: -16*(v[1]*(1-v[1])*v[0]*(1-v[0]))
    if fig=="parabola_with_forced_elevation":
        sol_exacte = lambda v: -16*(v[1]*(1-v[1])*v[0]*(1-v[0]))
    if fig=="pyramid": 
        sol_exacte = lambda v: 1- 2*np.linalg.norm(np.array([0.5-v[0],0.5-v[1]]),np.inf)
    if fig=="fig7":
        sol_exacte = lambda v: np.sin(2*np.pi*v[0])*np.sin(2*np.pi*v[1])
    if fig=="fig8":
        sol_exacte = lambda v: np.sin(2*np.pi*v[0])*np.sin(2*np.pi*v[1])
    if fig=="test":
        return 0
    for i in range(1,nb_pt-1):
        for j in range(1,nb_pt-1):
            count +=1
            res += np.abs(Un[i,j]-sol_exacte([x[i],y[i]]))
           
    res = res/(count)
    
    return res

# Methode du point fixe pour le probleme de SFS
def SFS_fixed_point_method(nb_pt=21,fig="parabola"):

    # Définition du maillage
    x = np.linspace(0,1,nb_pt)
    y = np.linspace(0,1,nb_pt)

    X,Y = np.meshgrid(x,y)
    Dx = x[1]-x[0]
    Dy = y[1]-y[0]
    Dt = Dx*Dy/np.sqrt(Dx**2+Dy**2)
    
    # Fonction de l'intensité lumineuse en fonction de la figure demandée
    if fig == "parabola":
        I = lambda v: 1 / np.sqrt(1 + (16 * v[1] * (1 - v[1]) * (1 - 2 * v[0]))**2 + (16 * v[0] * (1 - v[0]) * (1 - 2 * v[1]))**2)
    if fig == "reverse_parabola":
        I = lambda v: 1 / np.sqrt(1 + (16 * v[1] * (1 - v[1]) * (1 - 2 * v[0]))**2 + (16 * v[0] * (1 - v[0]) * (1 - 2 * v[1]))**2)
    if fig == "pyramid":
        I = lambda v: 1/np.sqrt(5)
    if fig == "parabola_with_forced_elevation":
        I = lambda v: 1 / np.sqrt(1 + (16 * v[1] * (1 - v[1]) * (1 - 2 * v[0]))**2 + (16 * v[0] * (1 - v[0]) * (1 - 2 * v[1]))**2)
    if fig == "fig7":
        I = lambda v: 1 / np.sqrt(1 + (2 * np.pi * np.sin(2 * np.pi * v[1]) * np.cos(2 * np.pi * v[0]))**2 + (2 * np.pi * np.sin(2 * np.pi * v[0]) * np.cos(2 * np.pi * v[1]))**2)
    if fig == "fig8":
        I = lambda v: 1 / np.sqrt(1 + (2 * np.pi * np.sin(2 * np.pi * v[1]) * np.cos(2 * np.pi * v[0]))**2 + (2 * np.pi * np.sin(2 * np.pi * v[0]) * np.cos(2 * np.pi * v[1]))**2)
    if fig == "test":
        I = lambda v: 1/np.sqrt(1+(2*v[0])**2)

    # Définition de la normale pour le SFS 
    n = lambda v: np.sqrt(1/I(v)**2 - 1)
    
    # Schéma de différence finie
    Dxp = lambda U, i, j: (U[i+1, j] - U[i, j]) / Dx
    Dxm = lambda U, i, j: (U[i, j] - U[i-1, j]) / Dx
    Dyp = lambda U, i, j: (U[i, j+1] - U[i, j]) / Dy
    Dym = lambda U, i, j: (U[i, j] - U[i, j-1]) / Dy

    # Les deux fonctions g et G du papier
    g = lambda i, j, a, b, c, d: np.sqrt(max(max(a, 0), max(-b, 0))**2 + max(max(c, 0), max(-d, 0))**2) - n((x[i], y[j]))
    G = lambda U, i, j: g(i, j, Dxm(U, i, j), Dxp(U, i, j), Dym(U, i, j), Dyp(U, i, j))

    #Initialisation de mon itération
    # Initialisation de mon itération
    Un = np.full((nb_pt, nb_pt), 0.0)  # U0 == 0
    #Un[:,0] = Un[:,-1] = 1
    #Un[0,:] = Un[-1,:] = x**2
    Up1= np.full((nb_pt,nb_pt), 0.0) 
    # Initialisation de mon itération
    
    #Up1[:,0] = Up1[:,-1] = 1
    #Up1[0,:] = Up1[-1,:] = x**2

    # Boucle itérative à modifier en while pour forcer la convergence en fonction d'un epsilon donné
    # Ici on fait 200 itérations, mais on peut demander plus (attention à la lenteur du code)
    
    for k in range(400):
        Un = Up1.copy()
        Un = cond(Un,nb_pt,fig)     #Applique les conditions pour les endroits où I(x)=1

        for i in range(1, nb_pt - 1):  
            for j in range(1, nb_pt - 1): 
                #Up1[i, j] = Un[i,j] - Dt* G(Un,i,j)      # methode du pt fixe
                if np.abs(np.minimum(Un[i-1,j],Un[i+1,j]) - np.minimum(Un[i,j-1],Un[i,j+1])) <= Dx * n([x[i],y[j]]):
                    Up1[i, j] = (np.minimum(Un[i-1,j],Un[i+1,j]) + np.minimum(Un[i,j-1],Un[i,j+1]) + np.sqrt( (np.minimum(Un[i-1,j],Un[i+1,j]) - np.minimum(Un[i,j-1],Un[i,j+1]))**2 + 2*Dx**2*n([x[i],y[j]])**2 ))/2
                else:
                    Up1[i, j] = n([x[i],y[j]])*Dx + np.minimum(np.minimum(Un[i-1,j],Un[i+1,j]),np.minimum(Un[i,j-1],Un[i,j+1]))
    Up1 = cond(Up1,nb_pt,fig)
    
    
    erreur_globale = erreur(Up1,nb_pt,fig,x,y)      # Calcul de l'erreur



    # ======== AFFICHAGE ======= #

    

    fig = plt.figure(figsize=(10, 4))  # 80% de l'écran
    ax = fig.add_subplot(1,2,1)
   
    # Calcul des valeurs de I sur le maillage
    Z = np.array([[I([X[i, j], Y[i, j]]) for j in range(X.shape[1])] for i in range(X.shape[0])])

    
    # Premier graphique
    contour1 = ax.contourf(X, Y, Z, levels=np.linspace(0,1,51), cmap='viridis', vmin=0, vmax=1)
    cbar = fig.colorbar(contour1, ax=ax, label='I(v)')
    cbar.set_ticks(np.linspace(0, 1, 5))
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Intensité lumineuse')
    
    
    # Deuxième figure
    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.plot_wireframe(X, Y, Up1, color='black', linewidth=1)
    surf = ax.plot_surface(X, Y, Up1, color='white', alpha=1)
    ax.view_init(elev=15, azim=-135)  
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlim(0, 1)
    ax.set_title('Shape reconstructed from the intensity')
    
    print(erreur_globale)
    ax.text2D(0.35, -0.1, f"Erreur: ${erreur_globale:.2e}$", transform=ax.transAxes)

    plt.show()
    


'''
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
''' 


SFS_fixed_point_method(nb_pt=51,fig="parabola") 