import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

def H(rho):
    return rho*(1-rho)

def Hp(rho):
    return 1 - 2*rho

def u0(x):
    return densite_init if x < -8 else densite_init

# Def variables
densite_init = 0.4
a = -10
b = 10
T=1e6
CFL=0.4
nb_maille = 100

# Def maillage
x = np.linspace(a, b, nb_maille+1)
dx = (b-a)/nb_maille
x_milieu = np.linspace(a+dx/2,b-dx/2,nb_maille)

def schema_generator(nb_maille, u0, a, b, f, fp, cfl, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    it = 0  # Compteur d'itérations pour les images de l'animation
    t = 0   # Variable de temps

    Uh = np.array([u0((x[i]+x[i+1])/2.0) for i in range(len(x)-1)])
    # Définition du flux
    def flux(um,up):
        return 0.5*(f(um)+f(up)) -0.5*(up - um)
    vectorized_flux = np.vectorize(flux)

    
    # Indice des feux
    i_feu_gauche = len(Uh) // 2 - len(Uh) // 4
    i_feu_centre = len(Uh) // 2
    i_feu_droite = len(Uh) // 2 + len(Uh) // 4
    feux = [ (i_feu_gauche, F_gauche), (i_feu_centre, F_centre), (i_feu_droite, F_droite) ]
    
    
    while t < T:
        Utemp = Uh.copy()

        Cn = np.max(np.abs(fp(Uh)))
        dt = cfl * dx / Cn

        if T - t < dt:
            dt = T - t
        t += dt

        # Mise à jour des valeurs intérieures
        Uh[1:-1] = (
            Uh[1:-1] 
            - dt/dx*(vectorized_flux(Uh[1:-1],Uh[2:])-vectorized_flux(Uh[:-2],Uh[1:-1]))
        )

        # Condition aux limites
        Uh[0] = Utemp[0] - dt/dx *(flux(Utemp[0],Utemp[1]) - flux(densite_init,Utemp[0]))
        Uh[-1] = Utemp[-1] - dt/dx * (flux(Utemp[-1],0.0) - flux(Utemp[-2],Utemp[-1]))

        # Calcul pour les feux rouges 
        for i_feu, F in feux:
            Uh[i_feu] = Utemp[i_feu] - dt / dx * (
                flux(Utemp[i_feu], Utemp[i_feu + 1]) - min(flux(Utemp[i_feu - 1], Utemp[i_feu]), F(t))
            )
            Uh[i_feu - 1] = Utemp[i_feu - 1] - dt / dx * (
                min(F(t), flux(Utemp[i_feu - 1], Utemp[i_feu])) - flux(Utemp[i_feu - 2], Utemp[i_feu - 1])
            )

        # On ne stocke que tous les 3 itérations pour alléger l'animation
        if it%3==0 or t+dt >= T:
            yield t, Uh.copy()
        
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
    return 0. if feu_droite["actif"] else densite_init



# Fonction pour l'animation interactive
def interactive_animation():
    gen = schema_generator(
        nb_maille, u0, a, b, f=H, fp=Hp, cfl=CFL, T=T
    )

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(a + 1, b - 1)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("x")
    ax.set_ylabel(r"$\rho(x,t)$")

    x_milieu = np.linspace(a + dx / 2, b - dx / 2, nb_maille)

    # Ajout de carrés vert pour les feux de circulation
    x_feu_gauche = x_milieu[nb_maille // 2 - nb_maille // 4]
    x_feu_centre = x_milieu[nb_maille // 2]
    x_feu_droite = x_milieu[nb_maille // 2 + nb_maille // 4]
    feu_rect_gauche = Rectangle((x_feu_gauche - dx, 0), dx, 0.1, color='green')
    feu_rect_centre = Rectangle((x_feu_centre - dx, 0), dx, 0.1, color='green')
    feu_rect_droite = Rectangle((x_feu_droite - dx, 0), dx, 0.1, color='green')
    ax.add_patch(feu_rect_gauche)
    ax.add_patch(feu_rect_centre)
    ax.add_patch(feu_rect_droite)

    def update(frame):
        try:
            t, Uh = next(gen)
            line.set_data(x_milieu, Uh)
            ax.set_title(f"Densité de voiture à t = {t:.2f}")
            # Mise à jour de la couleur du feu
            feu_rect_gauche.set_color('red' if feu_gauche["actif"] else 'green')
            feu_rect_centre.set_color('red' if feu_centre["actif"] else 'green')
            feu_rect_droite.set_color('red' if feu_droite["actif"] else 'green')
        except StopIteration:
            pass
        return line, feu_rect_centre, feu_rect_gauche, feu_rect_droite

    fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_connect('key_release_event', on_key_release)

    ani = animation.FuncAnimation(
        fig, update, interval=2, blit=False, frames=None, cache_frame_data=False
    )
    plt.show()


interactive_animation()
