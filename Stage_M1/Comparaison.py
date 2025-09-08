import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button


# ----------- Paramètres globaux ----------- #
a = -10
b = 10
nb_maille = 100
T = 1e3
C_CFL = 10
densite_init = 0.4

# ----------- Initialisation du maillage ----------- #
x = np.linspace(a, b, nb_maille + 1)
dx = x[1] - x[0]
x_milieu = (x[:-1] + x[1:]) / 2

# ----------- Fonction u0(x) et rho0(x) ----------- #
def u0(x):
    return densite_init*x if x < 0 else densite_init*x

U0 = np.array([u0(x[i]) for i in range(len(x))])

rho_0 = (U0[1:] - U0[:-1]) / dx     # Initialisation discrète de rho_0 

# ----------- Hamiltonien et flux de Godunov ----------- #
def H(p):
    return p * (1 - p)

def vectorized_g_H(p_minus, p_plus):
    p_star = 0.5
    cond1 = p_plus <= p_minus
    cond2 = (p_plus <= p_star) & (p_star <= p_minus)

    g = np.where(
        cond1,
        np.where(cond2, H(p_star), np.maximum(H(p_minus), H(p_plus))),
        np.minimum(H(p_minus), H(p_plus))
    )
    return g

# ----------- F_0 ----------- #
def G_plus(p):
    return H(p) if p < 1/2 else 1/4

def G_minus(p):
    return 1/4 if p < 1/2 else H(p)

def F_0(p_left,p_right,F): # Flux limité HJ
    return min(G_plus(p_left), G_minus(p_right),F)

# ----------- Schéma Hamilton-Jacobi ----------- #
def schema_HJ(T):

    it = 0 # Compteur d'itérations pour les images de l'animation
    t = 0   # Variable de temps

    Uh = U0.copy()  # Initialisation discrète de Uh avec U0

    # Indice des feux
    i_feu_gauche = len(Uh) // 2 - len(Uh) // 4
    i_feu_centre = len(Uh) // 2
    i_feu_droite = len(Uh) // 2 + len(Uh) // 4
    feux = [ (i_feu_gauche, F_gauche), (i_feu_centre, F_centre), (i_feu_droite, F_droite) ]

    while t < T:
        Utemp = Uh.copy()

        dt = dx / C_CFL

        if T - t < dt:
            dt = T - t
        t += dt


        # Mise à jour des valeurs intérieures avec schéma du papier
        Uh[1:-1] = (
            Uh[1:-1] - dt * vectorized_g_H((Utemp[1:-1] - Utemp[:-2]) / dx, (Utemp[2:] - Utemp[1:-1]) / dx)
        )
        
        # Condition aux limites
        Uh[0] = Utemp[0] - dt * vectorized_g_H(densite_init, (Utemp[1] - Utemp[0]) / dx)
        Uh[-1] = Utemp[-1] - dt * vectorized_g_H((Utemp[-1] - Utemp[-2]) / dx, 0.0)

        for i_feu, F in feux:
            Uh[i_feu] = (
                Utemp[i_feu] - dt * F_0(
                    (Utemp[i_feu]-Utemp[i_feu-1])/dx,
                    (Utemp[i_feu+1]-Utemp[i_feu])/dx,
                    F(t)
                )
            )

        # Stocke que tous les 30 itérations pour alléger l'animation
        if it % 30 == 0 or t + dt >= T:
            yield t, Uh.copy()

        it += 1

# ----------- Schéma conservation scalaire ----------- #
def conservation_law_solver(T):

    it = 0  # Compteur d'itérations pour les images de l'animation
    t = 0   # Variable de temps

    Rh = rho_0.copy()   # Initialisation discrète de Rh avec rho_0
    
    # Indice des feux
    i_feu_gauche = len(U0) // 2 - len(U0) // 4
    i_feu_centre = len(U0) // 2
    i_feu_droite = len(U0) // 2 + len(U0) // 4
    feux = [ (i_feu_gauche, F_gauche), (i_feu_centre, F_centre), (i_feu_droite, F_droite) ]
    
    
    while t < T:
        Rtemp = Rh.copy()

        dt = dx / C_CFL

        if T - t < dt:
            dt = T - t
        t += dt

        # Mise à jour des valeurs intérieures avec schéma du papier 
        Rh[1:-1] = (
            Rh[1:-1] 
            - dt/dx*(vectorized_g_H(Rh[1:-1],Rh[2:])-vectorized_g_H(Rh[:-2],Rh[1:-1]))
        )

        # Condition aux limites
        Rh[0] = Rtemp[0] - dt/dx *(vectorized_g_H(Rtemp[0],Rtemp[1]) - vectorized_g_H(densite_init,Rtemp[0]))
        Rh[-1] = Rtemp[-1] - dt/dx * (vectorized_g_H(Rtemp[-1],0.0) - vectorized_g_H(Rtemp[-2],Rtemp[-1]))

        # Calcul pour les feux rouges 
        for i_feu, F in feux:
            Rh[i_feu] = Rtemp[i_feu] - dt / dx * (
                vectorized_g_H(Rtemp[i_feu], Rtemp[i_feu + 1]) - F_0(Rtemp[i_feu-1],Rtemp[i_feu],F(t))
            )
            Rh[i_feu - 1] = Rtemp[i_feu - 1] - dt / dx * (
                F_0(Rtemp[i_feu - 1],Rtemp[i_feu],F(t)) - vectorized_g_H(Rtemp[i_feu - 2], Rtemp[i_feu - 1])
            )

        # On ne stocke que tous les 30 itérations pour alléger l'animation
        if it%30==0 or t+dt >= T:
            yield t, Rh.copy()
        
        it += 1


# ------- VF_circulation---------- #
def schema_generator(f, T):

    it = 0  # Compteur d'itérations pour les images de l'animation
    t = 0   # Variable de temps

    Rh = rho_0.copy()   # Initialisation discrète de Rh avec rho_0 
    
    # Définition du flux
    def flux(um,up):
        return 0.5*(f(um)+f(up)) -0.5*(up - um)
    vectorized_flux = np.vectorize(flux)

    
    # Indice des feux
    i_feu_gauche = len(Rh) // 2 - len(Rh) // 4
    i_feu_centre = len(Rh) // 2
    i_feu_droite = len(Rh) // 2 + len(Rh) // 4
    feux = [ (i_feu_gauche, F_gauche), (i_feu_centre, F_centre), (i_feu_droite, F_droite) ]
    
    
    while t < T:
        Rtemp = Rh.copy()

        dt = dx / C_CFL

        if T - t < dt:
            dt = T - t
        t += dt

        # Mise à jour des valeurs intérieures méthode VF
        Rh[1:-1] = (
            Rh[1:-1] 
            - dt/dx*(vectorized_flux(Rh[1:-1],Rh[2:])-vectorized_flux(Rh[:-2],Rh[1:-1]))
        )

        # Condition aux limites
        Rh[0] = Rtemp[0] - dt/dx *(flux(Rtemp[0],Rtemp[1]) - flux(densite_init,Rtemp[0]))
        Rh[-1] = Rtemp[-1] - dt/dx * (flux(Rtemp[-1],0.0) - flux(Rtemp[-2],Rtemp[-1]))

        # Calcul pour les feux rouges 
        for i_feu, F in feux:
            Rh[i_feu] = Rtemp[i_feu] - dt / dx * (
                flux(Rtemp[i_feu], Rtemp[i_feu + 1]) - min(flux(Rtemp[i_feu - 1], Rtemp[i_feu]), F(t))
            )
            Rh[i_feu - 1] = Rtemp[i_feu - 1] - dt / dx * (
                min(F(t), flux(Rtemp[i_feu - 1], Rtemp[i_feu])) - flux(Rtemp[i_feu - 2], Rtemp[i_feu - 1])
            )

        # On ne stocke que tous les 30 itérations pour alléger l'animation
        if it%30==0 or t+dt >= T:
            yield t, Rh.copy()
        
        it += 1


# ====== Fonctions pour une simulation de feux rouges intéractifs ====== #
feu_gauche = {"actif": False}
feu_centre = {"actif": False}
feu_droite = {"actif": False}

def on_key_press(event):
    if event.key == 'a':
        feu_gauche["actif"] = True
    elif event.key == 'z':
        feu_centre["actif"] = True
    elif event.key == 'e':
        feu_droite["actif"] = True

def on_key_release(event):
    if event.key == 'a':             
        feu_gauche["actif"] = False
    elif event.key == 'z':             
        feu_centre["actif"] = False
    elif event.key == 'e':             
        feu_droite["actif"] = False

def F_gauche(t):
    return 0 if feu_gauche["actif"] else densite_init
def F_centre(t):
    return 0 if feu_centre["actif"] else densite_init
def F_droite(t):
    return 0 if feu_droite["actif"] else densite_init


# ----------- Dérivée discrète ----------- #
def discrete_derivative(Uh, dx):
    dUh = (Uh[1:]-Uh[:-1]) / dx
    return dUh

# ----------- Animation de la comparaison ----------- #
def animate_comparison():
    gen_hj_papier = schema_HJ(T=T)
    gen_cons_papier = conservation_law_solver(T=T)
    sch_gen = schema_generator(f=H, T=T)

    fig, ax = plt.subplots()
    line_hj, = ax.plot([], [], 'b-', label=r"$\partial_x u$ (HJ)")
    line_cons, = ax.plot([], [], 'r--', label=r"$\rho$ papier")
    line_u, = ax.plot([],[], 'g--', label=r"$u$")
    line_sch, = ax.plot([], [],  color='orange', linestyle='-', label=r"$\rho$ volume fini classique")
    ax.set_xlim(a , b ) 
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("Densité")
    ax.set_title(r"Comparaison : dérivée de $u$ vs $\rho$")
    ax.legend()

    # Feux rouges
    rect_width = 0.5
    x_feu_gauche = x_milieu[nb_maille // 2 - nb_maille // 4]
    x_feu_centre = x_milieu[nb_maille // 2]
    x_feu_droite = x_milieu[nb_maille // 2 + nb_maille // 4]

    feu_rect_gauche = Rectangle((x_feu_gauche - rect_width/2, 0), rect_width, 0.1, color='green')
    feu_rect_centre = Rectangle((x_feu_centre - rect_width/2, 0), rect_width, 0.1, color='green')
    feu_rect_droite = Rectangle((x_feu_droite - rect_width/2, 0), rect_width, 0.1, color='green')
    #ax.add_patch(feu_rect_gauche)
    ax.add_patch(feu_rect_centre)
    #ax.add_patch(feu_rect_droite)

    def update(frame):
        try:
            # Calcul de la solution à chaque pas de temps
            t1, Uh = next(gen_hj_papier)
            line_u.set_data(x, Uh)
            t2, rho = next(gen_cons_papier)
            line_cons.set_data(x_milieu, rho)
            rho_from_HJ = discrete_derivative(Uh, dx)
            line_hj.set_data(x_milieu, rho_from_HJ)
            t3, rho_sch = next(sch_gen)
            line_sch.set_data(x_milieu, rho_sch)
            
            # Modifie l'affichage à chaque pas de temps
            ax.set_title(f"Circulation routière à t = {t1:.2f}")
            feu_rect_gauche.set_color('red' if feu_gauche["actif"] else 'green')
            feu_rect_centre.set_color('red' if feu_centre["actif"] else 'green')
            feu_rect_droite.set_color('red' if feu_droite["actif"] else 'green')
        except StopIteration:
            pass
        return line_cons, line_u, line_hj, line_sch ,

    # Détection des pressions de touches pour les feux rouges
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_connect('key_release_event', on_key_release)
    
    ani = animation.FuncAnimation(
        fig, update, interval=30, blit=False, frames=None, cache_frame_data=False
    )
    plt.show()

# ----------- Lancer l’animation ----------- #
if __name__ == "__main__":
    animate_comparison()
