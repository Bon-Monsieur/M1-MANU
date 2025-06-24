import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button


# ----------- Paramètres globaux ----------- #
a = -10
b = 10
nb_maille = 50
dx = (b - a) / nb_maille
T = 1e3
CFL = 0.1
densite_init = 0.4

x = np.linspace(a, b, nb_maille + 1)
x_milieu = np.linspace(a + dx/2, b - dx/2, nb_maille)

# ----------- Fonction u0(x) et rho0(x) ----------- #
def u0(x):
    return 0.4*x if x < 0 else 0.0

def rho0(x,dx):
    return (u0(x+dx)-u0(x))/dx

# ----------- Hamiltonien et flux de Godunov ----------- #
def H(p):
    return p * (1 - p)

def H_prime(p):
    return 1 - 2 * p

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

def g_H(a, b):
    return max(H(min(a, b)), H(max(a, b))) if a <= b else max(H(a), H(b))

# ----------- F_0 ----------- #
def H_plus(p):
    return 1/4 if p < 1/2 else H(p)

def H_minus(p):
    return 1/4 if p > 1/2 else H(p)

def F_0(p_left,p_right,F): # Flux limité HJ
    return min(H_plus(p_right), H_minus(p_left),F)


# ----------- Schéma Hamilton-Jacobi ----------- #
def schema_HJ(nb_maille, u0, a, b, f, fp, cfl, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    it = 0
    t = 0

    Uh = np.array([u0(x[i]) for i in range(len(x))])

    # Indice des feux
    i_feu_gauche = len(Uh) // 2 - len(Uh) // 4
    i_feu_centre = len(Uh) // 2
    i_feu_droite = len(Uh) // 2 + len(Uh) // 4
    feux = [ (i_feu_gauche, F_gauche), (i_feu_centre, F_centre), (i_feu_droite, F_droite) ]

    while t < T:
        Utemp = Uh.copy()

        dt = dx / 42

        if T - t < dt:
            dt = T - t
        t += dt

        Uh[1:-1] = (
            Uh[1:-1] - dt * vectorized_g_H((Utemp[1:-1] - Utemp[:-2]) / dx, (Utemp[2:] - Utemp[1:-1]) / dx)
        )
        
        # Condition aux limites
        u_gauche = Utemp[0] - 0.4 * dx
        Uh[0] = Utemp[0] - dt * vectorized_g_H((Utemp[0] - u_gauche) / dx, (Utemp[1] - Utemp[0]) / dx)
        Uh[-1] = Utemp[-1] - dt * vectorized_g_H((Utemp[-1] - Utemp[-2]) / dx, 0.0)

        for i_feu, F in feux:
            Uh[i_feu] = Utemp[i_feu] - dt * F_0(
                (Utemp[i_feu]-Utemp[i_feu-1])/dx,
                (Utemp[i_feu+1]-Utemp[i_feu])/dx,
                F(t)
                )


        if it % 30 == 0 or t + dt >= T:
            yield t, Uh.copy()

        it += 1

# ----------- Schéma conservation scalaire ----------- #
def conservation_law_solver(nb_maille, Rho0, a, b,f,fp,cfl, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    it = 0  # Compteur d'itérations pour les images de l'animation
    t = 0   # Variable de temps

    Rh = np.array([Rho0((x[i]+x[i+1])/2.0,dx) for i in range(len(x)-1)])
    
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
                vectorized_g_H(Rtemp[i_feu], Rtemp[i_feu + 1]) - F_0(Rtemp[i_feu-1],Rtemp[i_feu],F(t))#- min(vectorized_g_H(Rtemp[i_feu - 1], Rtemp[i_feu]), F(t))
            )
            Rh[i_feu - 1] = Rtemp[i_feu - 1] - dt / dx * (
                F_0(Rtemp[i_feu - 1],Rtemp[i_feu],F(t)) - vectorized_g_H(Rtemp[i_feu - 2], Rtemp[i_feu - 1]) #min(F(t), vectorized_g_H(Rtemp[i_feu - 1], Rtemp[i_feu]))
            )

        # On ne stocke que tous les 3 itérations pour alléger l'animation
        if it%30==0 or t+dt >= T:
            yield t, Rh.copy()
        
        it += 1


# ------- test ---------- #
def schema_generator(nb_maille, Rho0, a, b, f, fp, cfl, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    it = 0  # Compteur d'itérations pour les images de l'animation
    t = 0   # Variable de temps

    Rh = np.array([Rho0((x[i]+x[i+1])/2.0,dx) for i in range(len(x)-1)])
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

        dt = dx / 42

        if T - t < dt:
            dt = T - t
        t += dt

        # Mise à jour des valeurs intérieures
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


# ----------- Dérivée discrète ----------- #
def discrete_derivative(Uh, dx):
    dUh = [(Uh[i+1] - Uh[i]) /  dx for i in range(0, len(Uh)-1)]
    return dUh

# ----------- Animation de la comparaison ----------- #
def animate_comparison():
    gen_hj = schema_HJ(nb_maille, u0, a, b, H, H_prime, cfl=CFL, T=T)
    gen_cons = conservation_law_solver(nb_maille, rho0, a, b, H, H_prime, cfl=CFL, T=T)
    sch_gen = schema_generator(nb_maille, rho0, a, b, H, H_prime, cfl=CFL, T=T)

    fig, ax = plt.subplots()
    x_milieu = np.linspace(a + dx / 2, b - dx / 2, nb_maille)
    Rh_init = np.array([rho0(xi,dx) for xi in x_milieu])

    line_hj, = ax.plot([], [], 'b-', label=r"$\partial_x u$ (HJ)")
    line_cons, = ax.plot([], [], 'r--', label=r"$\rho$ (conservation)")
    #line_u, = ax.plot([],[], 'g--', label=r"$u$")
    line_sch, = ax.plot([], [],  color='orange', linestyle='-', label=r"$\rho$ volume fini")
    ax.set_xlim(a+1 , b-1 )
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("Valeur")
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
    ax.add_patch(feu_rect_gauche)
    ax.add_patch(feu_rect_centre)
    ax.add_patch(feu_rect_droite)

    def update(frame):
        try:
            t1, Uh = next(gen_hj)
            #line_u.set_data(x, Uh)
            t2, rho = next(gen_cons)
            line_cons.set_data(x_milieu, rho)
            rho_from_HJ = discrete_derivative(Uh, dx)
            line_hj.set_data(x_milieu, rho_from_HJ)
            t3, rho_sch = next(sch_gen)
            line_sch.set_data(x_milieu, rho_sch)
            ax.set_title(f"Comparaison à t = {t1:.2f}")
        except StopIteration:
            pass
        return line_hj, line_cons, line_sch #, line_u

    fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_connect('key_release_event', on_key_release)
    
    ani = animation.FuncAnimation(
        fig, update, interval=2, blit=False, frames=None, cache_frame_data=False
    )
    plt.show()

# ----------- Lancer l’animation ----------- #
if __name__ == "__main__":
    animate_comparison()
