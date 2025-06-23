import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

def H(rho):
    return rho*(1-rho)

def Hp(rho):
    return 1 - 2*rho

def V(rho): # Vitesse instantannée
    return 1 - rho

def Rho0(x):
    return 0.4 if x < 0.0 else 0.0

def vectorized_g_H(p_minus, p_plus):
    p_star = 0.5
    f_p_minus = H(p_minus)
    f_p_plus = H(p_plus)
    f_p_star = H(p_star)

    cond1 = p_plus <= p_minus
    cond2 = (p_plus <= p_star) & (p_star <= p_minus)

    g = np.where(
        cond1,
        np.where(cond2, f_p_star, np.maximum(f_p_minus, f_p_plus)),
        np.minimum(f_p_minus, f_p_plus)
    )
    return g

# Def variables
densite_init = 0.4
a = -5
b = 5
T=1e3
nb_maille = 200

# Def maillage
x = np.linspace(a, b, nb_maille+1)
dx = (b-a)/nb_maille
x_milieu = np.linspace(a+dx/2,b-dx/2,nb_maille)

def schema_generator(nb_maille, Rho0, a, b, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    it = 0  # Compteur d'itérations pour les images de l'animation
    t = 0   # Variable de temps

    Rh = np.array([Rho0((x[i]+x[i+1])/2.0) for i in range(len(x)-1)])
    
    # Indice des feux
    i_feu_gauche = len(Rh) // 2 - len(Rh) // 4
    i_feu_centre = len(Rh) // 2
    i_feu_droite = len(Rh) // 2 + len(Rh) // 4
    feux = [ (i_feu_gauche, F_gauche), (i_feu_centre, F_centre), (i_feu_droite, F_droite) ]
    
    
    while t < T:
        Rtemp = Rh.copy()

        dt = dx / 42

        if T - t < dt:
            dt = T - t
        t += dt

        # Mise à jour des valeurs intérieures
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
                vectorized_g_H(Rtemp[i_feu], Rtemp[i_feu + 1]) - min(vectorized_g_H(Rtemp[i_feu - 1], Rtemp[i_feu]), F(t))
            )
            Rh[i_feu - 1] = Rtemp[i_feu - 1] - dt / dx * (
                min(F(t), vectorized_g_H(Rtemp[i_feu - 1], Rtemp[i_feu])) - vectorized_g_H(Rtemp[i_feu - 2], Rtemp[i_feu - 1])
            )

        # On ne stocke que tous les 3 itérations pour alléger l'animation
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



from matplotlib.widgets import Button

def interactive_animation():
    gen = schema_generator(nb_maille, Rho0, a, b, T=T)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [2, 2]})
    fig.subplots_adjust(bottom=0.25, hspace=0.4)


    fig.suptitle("Simulation de circulation avec feux rouges interactifs", fontsize=12)

    x_milieu = np.linspace(a + dx / 2, b - dx / 2, nb_maille)
    Rh_init = np.array([Rho0(xi) for xi in x_milieu])

    line1, = ax1.plot(x_milieu, Rh_init, lw=2, label=r'$\rho(t,x)$')
    ax1.set_xlim(a + 1, b - 1)
    ax1.set_ylim(0, 1.2)
    ax1.set_title("Densité de voiture")
    ax1.legend(loc='upper right')

    line2, = ax2.plot(x_milieu, H(Rh_init), lw=2, label=r'$f(\rho(t,x))$',color='green')
    line3, = ax2.plot(x_milieu, V(Rh_init), lw=2, label=r'$V(\rho(t,x))$',color='orange')
    ax2.set_xlim(a + 1, b - 1)
    ax2.set_ylim(0, 1.2)
    ax2.set_title("Flux et vitesse potentielle")
    ax2.set_xlabel("x")
    ax2.legend(loc='upper right', ncol=2)

    # Feux rouges
    rect_width = 0.5
    x_feu_gauche = x_milieu[nb_maille // 2 - nb_maille // 4]
    x_feu_centre = x_milieu[nb_maille // 2]
    x_feu_droite = x_milieu[nb_maille // 2 + nb_maille // 4]

    feu_rect_gauche = Rectangle((x_feu_gauche - rect_width/2, 0), rect_width, 0.1, color='green')
    feu_rect_centre = Rectangle((x_feu_centre - rect_width/2, 0), rect_width, 0.1, color='green')
    feu_rect_droite = Rectangle((x_feu_droite - rect_width/2, 0), rect_width, 0.1, color='green')
    ax1.add_patch(feu_rect_gauche)
    ax1.add_patch(feu_rect_centre)
    ax1.add_patch(feu_rect_droite)

    # === Contrôle de simulation === #
    history = [(0, Rh_init)]
    frame_index = {"value": 0}
    running = {"value": False}

    def update_display(t, Rh):
        line1.set_data(x_milieu, Rh)
        line2.set_data(x_milieu, H(Rh))
        line3.set_data(x_milieu, V(Rh))
        feu_rect_gauche.set_color('red' if feu_gauche["actif"] else 'green')
        feu_rect_centre.set_color('red' if feu_centre["actif"] else 'green')
        feu_rect_droite.set_color('red' if feu_droite["actif"] else 'green')

    def update(frame):
        if running["value"]:
            try:
                t, Rh = next(gen)
                history.append((t, Rh))
                history.append((t, Rh))
                if len(history) > 10:
                    history.pop(0)  # Supprime le plus ancien

                frame_index["value"] += 1
                update_display(t, Rh)
            except StopIteration:
                running["value"] = False
        else:
            if 0 <= frame_index["value"] < len(history):
                t, Rh = history[frame_index["value"]]
                update_display(t, Rh)

        return line1, line2, line3, feu_rect_centre, feu_rect_gauche, feu_rect_droite

    fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_connect('key_release_event', on_key_release)

    ani = animation.FuncAnimation(
        fig, update, interval=2, blit=True, frames=None, cache_frame_data=False
    )

    # Bouton Play/Pause
    ax_playpause = plt.axes([0.05, 0.05, 0.2, 0.075])
    btn_playpause = Button(ax_playpause, '▶ Démarrer')

    # Bouton Reset
    ax_reset = plt.axes([0.275, 0.05, 0.2, 0.075])
    btn_reset = Button(ax_reset, 'Réinitialiser')

    # Bouton Précédent
    ax_prev = plt.axes([0.5, 0.05, 0.2, 0.075])
    btn_prev = Button(ax_prev, 'Précédent')

    # Bouton Suivant
    ax_next = plt.axes([0.725, 0.05, 0.2, 0.075])
    btn_next = Button(ax_next, 'Suivant')


    def on_playpause(event):
        running["value"] = not running["value"]
        btn_playpause.label.set_text("Pause" if running["value"] else "▶ Démarrer")

    def on_reset(event):
        nonlocal gen
        running["value"] = False
        btn_playpause.label.set_text("▶ Démarrer")
        gen = schema_generator(nb_maille, Rho0, a, b, T=T)
        history.clear()
        history.append((0, Rh_init))
        Rh_init = np.array([Rho0(xi) for xi in x_milieu])
        history.append((0, Rh_init))
        frame_index["value"] = 0
        update_display(0, Rh_init)

    def on_prev(event):
        running["value"] = False
        if frame_index["value"] > 0:
            frame_index["value"] -= 1
            t, Rh = history[frame_index["value"]]
            update_display(t, Rh)

    def on_next(event):
        running["value"] = False
        if frame_index["value"] < len(history) - 1:
            # Aller à l'image suivante déjà calculée
            frame_index["value"] += 1
            t, Rh = history[frame_index["value"]]
            update_display(t, Rh)
        else:
            try:
                # Générer une nouvelle image si on est à la fin de l'historique
                t, Rh = next(gen)
                history.append((t, Rh))
                frame_index["value"] += 1
                update_display(t, Rh)
            except StopIteration:
                pass  # Plus d'image à générer

    btn_playpause.on_clicked(on_playpause)
    btn_reset.on_clicked(on_reset)
    btn_prev.on_clicked(on_prev)
    btn_next.on_clicked(on_next)

    plt.show()

interactive_animation()
