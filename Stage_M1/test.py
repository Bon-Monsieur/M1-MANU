import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from matplotlib.widgets import Button

def f(u):
    return u*(1-u)

def fp(u):
    return 1 - 2*u

def u0(x):
    return 1/20*x+0.5

def g_H(p_minus, p_plus):
    if p_minus <= p_plus:
        p_star = 0.5
        if p_minus <= p_star <= p_plus:
            return f(p_star)
        else:
            return min(f(p_minus), f(p_plus))
    else:
        return max(f(p_minus), f(p_plus)) 
    
vectorized_g_H = np.vectorize(g_H)

# Def variables
densite_init = 0.4
a = -10
b = 10
T=1e3
CFL=0.1
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
            - dt*(vectorized_g_H((Utemp[1:-1]-Utemp[:-2])/dx,(Utemp[2:]-Utemp[1:-1])/dx))
        )

        # Condition aux limites
        Uh[0] = densite_init
        Uh[-1] = Utemp[-1]

        # On ne stocke que tous les 3 itérations pour alléger l'animation
        if it%10==0 or t+dt >= T:
            yield t, Uh.copy()
        
        it += 1


def interactive_animation():
    gen = schema_generator(
        nb_maille, u0, a, b, f, fp, cfl=CFL, T=T
    )

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2, label=r"$u(t,x)$")
    line2, = ax.plot([], [], lw=2,label=r"$\partial_x u(t,x)$")
    ax.set_xlim(a , b )
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("x")
    ax.set_title(f"Resolution HJ")
    ax.set_ylabel(r"$u(x,t)$")
    ax.legend()

    x_milieu = np.linspace(a + dx / 2, b - dx / 2, nb_maille)

    def update(frame):
        try:
            t, Uh = next(gen)
            line.set_data(x_milieu, Uh)
            dUh = discrete_derivative(Uh, dx)
            line2.set_data(x_milieu[1:-1], dUh[1:-1])
        except StopIteration:
            pass
        return line, line2

    ani = animation.FuncAnimation(
        fig, update, interval=10, blit=True, frames=None,cache_frame_data=False
    )
    plt.show()

def discrete_derivative(Uh, dx):
    dUh = np.ones_like(Uh)*0.4
    dUh[1:-1] = (Uh[2:] - Uh[:-2]) / (2 * dx)
    dUh[0] = (Uh[1] - Uh[0]) / dx
    dUh[-1] = (Uh[-1] - Uh[-2]) / dx
    return dUh


interactive_animation()