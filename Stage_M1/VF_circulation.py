import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

def f(rho):
    return rho*(1-rho)

def fp(rho):
    return 1 - 2*rho

def V(rho):
    return 1 - rho

def u0(x):
    return densite_init if x < -8 else densite_init

# Def variables
densite_init = 0.4
a = -10
b = 10
T=1e3
CFL=0.25
nb_maille = 200

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
        if it%10==0 or t+dt >= T:
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
    return 0 if feu_droite["actif"] else densite_init



# Fonction pour l'animation interactive
def interactive_animation():
    gen = schema_generator(
        nb_maille, u0, a, b, f=f, fp=fp, cfl=CFL, T=T
    )

    # Deux sous-graphes verticaux
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8), sharex=True)

    # Courbe 1 : densité sur ax1
    line1, = ax1.plot([], [], lw=2, label='Densité de voiture')
    ax1.set_xlim(a + 1, b - 1)
    ax1.set_ylim(0, 1.2)
    ax1.set_ylabel(r"$\rho(x,t)$")
    ax1.set_title(f"Simulation de circulation (densité)")
    ax1.legend(loc='upper right')

    # Courbes 2 & 3 : flux et vitesse sur ax2
    line2, = ax2.plot([], [], lw=2, label=r'$f(\rho(t,x))$')
    line3, = ax2.plot([], [], lw=2, label=r'$V(\rho(t,x))$')
    ax2.set_xlim(a + 1, b - 1)
    ax2.set_ylim(0, 1.2)
    ax2.set_xlabel("x")
    ax2.set_ylabel("Flux / Vitesse")
    ax2.set_title("Flux et vitesse en fonction de la densité")
    ax2.legend(loc='upper right', ncol=2)

    x_milieu = np.linspace(a + dx / 2, b - dx / 2, nb_maille)

    # Feux rouges sur le subplot de la densité
    x_feu_gauche = x_milieu[nb_maille // 2 - nb_maille // 4]
    x_feu_centre = x_milieu[nb_maille // 2]
    x_feu_droite = x_milieu[nb_maille // 2 + nb_maille // 4]
    rect_width = 0.5  # Largeur fixe en unités de données

    feu_rect_gauche = Rectangle(
        (x_feu_gauche - rect_width / 2, 0),  # centré en x
        rect_width, 0.1,
        color='green'
    )
    feu_rect_centre = Rectangle(
        (x_feu_centre - rect_width / 2, 0),
        rect_width, 0.1,
        color='green'
    )
    feu_rect_droite = Rectangle(
        (x_feu_droite - rect_width / 2, 0),
        rect_width, 0.1,
        color='green'
    )
    ax1.add_patch(feu_rect_gauche)
    ax1.add_patch(feu_rect_centre)
    ax1.add_patch(feu_rect_droite)

    def update(frame):
        try:
            t, Uh = next(gen)
            line1.set_data(x_milieu, Uh)
            line2.set_data(x_milieu, f(Uh))
            line3.set_data(x_milieu, V(Uh))            
            feu_rect_gauche.set_color('red' if feu_gauche["actif"] else 'green')
            feu_rect_centre.set_color('red' if feu_centre["actif"] else 'green')
            feu_rect_droite.set_color('red' if feu_droite["actif"] else 'green')
        except StopIteration:
            pass
        return line1, line2, line3, feu_rect_centre, feu_rect_gauche, feu_rect_droite

    fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_connect('key_release_event', on_key_release)

    ani = animation.FuncAnimation(
        fig, update, interval=20, blit=True, frames=None, cache_frame_data=False
    )
    
    plt.show()



interactive_animation()
