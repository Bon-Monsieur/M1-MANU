import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle

def H(rho):
    return rho*(1-rho)

def Hp(rho):
    return 1 - 2*rho

def u0(x):
    return densite_init

# Def variables
densite_init = 0.4
a = -10
b = 10
T=250
nb_maille = 100

# Def maillage
x = np.linspace(a, b, nb_maille+1)
dx = (b-a)/nb_maille
x_milieu = np.linspace(a+dx/2,b-dx/2,nb_maille)

def schema_generator(nb_maille, u0, a, b, f, fp, cfl, T, F):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    Uh = np.array([u0((x[i]+x[i+1])/2.0) for i in range(len(x)-1)])

    it = 0
    t = 0
    i_centre = len(Uh) // 2

    # Definition du flux
    def flux(um,up):
        return 0.5*(f(um)+f(up)) -0.5*(up - um)
    vectorized_flux = np.vectorize(flux)

    while t < T:
        Cn = np.max(np.abs(fp(Uh)))
        dt = cfl * dx / Cn

        if T - t < dt:
            dt = T - t
        t += dt
        it += 1

        Utemp = Uh.copy()
        Uh[0] = Utemp[0] - dt/dx *(flux(Utemp[0],Utemp[1]) - flux(densite_init,Utemp[0]))
        Uh[-1] = Utemp[-1] - dt/dx * (flux(Utemp[-1],0.25) - flux(Utemp[-2],Utemp[-1]))
        Uh[1:-1] = (
            Uh[1:-1] 
            - dt/dx*(vectorized_flux(Uh[1:-1],Uh[2:])-vectorized_flux(Uh[:-2],Uh[1:-1]))
        )
        Uh[i_centre] = Utemp[i_centre] - dt / dx * (
                    flux(Utemp[i_centre], Utemp[i_centre+1]) - min(flux(Utemp[i_centre-1], Utemp[i_centre]),F(t))
                )
        Uh[i_centre-1] = Utemp[i_centre-1] - dt / dx * (
                    min(F(t),flux(Utemp[i_centre-1], Utemp[i_centre])) -  flux(Utemp[i_centre-2], Utemp[i_centre-1])
                )

        if it%3==0 or t+dt >= T:
            yield t, Uh.copy()


# ====== Fonctions pour une simulation de feu rouge intéractif ====== #
feu_rouge = {"actif": False}

def on_key_press(event):
    if event.key == ' ':
        feu_rouge["actif"] = True

def on_key_release(event):
    if event.key == ' ':             
        feu_rouge["actif"] = False

def F_dyn(t):
    return 0 if feu_rouge["actif"] else densite_init



def interactive_animation():
    gen = schema_generator(
        nb_maille, u0, a, b, H, Hp, cfl=0.25, T=T, F=F_dyn
    )

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(a + 1, b - 1)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("x")
    ax.set_ylabel(r"$\rho(x,t)$")

    x_milieu = np.linspace(a + dx / 2, b - dx / 2, nb_maille)

    # ➕ Ajout du carré (position approximative du feu)
    x_feu = x_milieu[nb_maille // 2]
    feu_rect = Rectangle((x_feu - dx/2, 0), dx, 0.1, color='green')
    ax.add_patch(feu_rect)

    def update(frame):
        try:
            t, Uh = next(gen)
            line.set_data(x_milieu, Uh)
            ax.set_title(f"Densité à t = {t:.2f} | Feu {'rouge' if feu_rouge['actif'] else 'vert'}")
            # 🔁 Mise à jour de la couleur du feu
            feu_rect.set_color('red' if feu_rouge["actif"] else 'green')
        except StopIteration:
            pass
        return line, feu_rect

    fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_connect('key_release_event', on_key_release)

    ani = animation.FuncAnimation(
        fig, update, interval=2, blit=False
    )
    plt.show()


interactive_animation()
