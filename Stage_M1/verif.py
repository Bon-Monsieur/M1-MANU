import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ----------- Paramètres globaux ----------- #
a = -10
b = 10
nb_maille = 200
dx = (b - a) / nb_maille
T = 1e3
CFL = 0.1

x = np.linspace(a, b, nb_maille + 1)
x_milieu = np.linspace(a + dx/2, b - dx/2, nb_maille)

# ----------- Fonction u0(x) et rho0(x) ----------- #
def u0(x):
    return x*0.4 if x < 0 else 0.0

def rho0(x,dx):
    return (u0(x+dx)-u0(x))/dx

# ----------- Hamiltonien et flux de Godunov ----------- #
def H(p):
    return p * (1 - p)

def H_prime(p):
    return 1 - 2 * p

def g_H(p_minus, p_plus):
    p_star = 0.5
    if p_plus <= p_minus:
        if p_plus <= p_star <= p_minus:
            return H(p_star)
        else:
            return max(H(p_minus), H(p_plus))
    else:
        return min(H(p_minus), H(p_plus))


vectorized_g_H = np.vectorize(g_H)

# ----------- Schéma Hamilton-Jacobi ----------- #
def schema_HJ(nb_maille, u0, a, b, f, fp, cfl, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    it = 0
    t = 0

    Uh = np.array([u0(x[i]) for i in range(len(x) - 1)])

    while t < T:
        Utemp = Uh.copy()

        dt = dx / 50

        if T - t < dt:
            dt = T - t
        t += dt

        Uh[1:-1] = (
            Uh[1:-1] - dt * vectorized_g_H((Utemp[1:-1] - Utemp[:-2]) / dx, (Utemp[2:] - Utemp[1:-1]) / dx)
        )

        # Conditions aux bords
        Uh[0] = Utemp[0] - dt * vectorized_g_H((Utemp[0]-0.4)/dx, (Utemp[1]-Utemp[0])/dx)
        Uh[-1] = Utemp[-1] - dt * vectorized_g_H((Utemp[-1]-Utemp[-2])/dx, (0.0 - Utemp[-1])/dx)

        if it % 10 == 0 or t + dt >= T:
            yield t, Uh.copy()

        it += 1

# ----------- Schéma conservation scalaire ----------- #
def conservation_law_solver(nb_maille, Rho0, a, b, f, fp, cfl, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    it = 0  # Compteur d'itérations pour les images de l'animation
    t = 0   # Variable de temps

    Rh = np.array([Rho0((x[i]+x[i+1])/2.0,dx) for i in range(len(x)-1)])
    
    
    while t < T:
        Rtemp = Rh.copy()

        dt = dx / 50

        if T - t < dt:
            dt = T - t
        t += dt

        # Mise à jour des valeurs intérieures
        Rh[1:-1] = (
            Rh[1:-1] 
            - dt/dx*(vectorized_g_H(Rh[1:-1],Rh[2:])-vectorized_g_H(Rh[:-2],Rh[1:-1]))
        )

        # Condition aux limites
        Rh[0] = Rtemp[0] - dt/dx *(vectorized_g_H(Rtemp[0],Rtemp[1]) - vectorized_g_H(0.4,Rtemp[0]))
        Rh[-1] = Rtemp[-1] - dt/dx * (vectorized_g_H(Rtemp[-1],0.0) - vectorized_g_H(Rtemp[-2],Rtemp[-1]))


        # On ne stocke que tous les 3 itérations pour alléger l'animation
        if it%10==0 or t+dt >= T:
            yield t, Rh.copy()
        
        it += 1

# ----------- Dérivée discrète centrée ----------- #
def discrete_derivative(Uh, dx):
    dUh = np.zeros_like(Uh)
    dUh[1:-1] = (Uh[2:] - Uh[1:-1]) / dx
    dUh[0]= (Uh[1] - Uh[0]) / dx
    dUh[-1] = (0.0 - Uh[-1]) / dx
    return dUh

# ----------- Animation de la comparaison ----------- #
def animate_comparison():
    gen_hj = schema_HJ(nb_maille, u0, a, b, H, H_prime, cfl=CFL, T=T)
    gen_cons = conservation_law_solver(nb_maille, rho0, a, b, H, H_prime, cfl=CFL, T=T)

    fig, ax = plt.subplots()
    line_hj, = ax.plot([], [], 'b-', label=r"$\partial_x u$ (HJ)")
    line_cons, = ax.plot([], [], 'r--', label=r"$\rho$ (conservation)")
    line_u, = ax.plot([],[], 'g--', label=r"$u$")
    ax.set_xlim(a+1 , b-1 )
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("Valeur")
    ax.set_title(r"Comparaison : dérivée de $u$ vs $\rho$")
    ax.legend()

    def update(frame):
        try:
            t1, Uh = next(gen_hj)
            line_u.set_data(x_milieu, Uh)
            t2, rho = next(gen_cons)
            line_cons.set_data(x_milieu, rho)
            rho_from_HJ = discrete_derivative(Uh, dx)
            line_hj.set_data(x_milieu, rho_from_HJ)
            ax.set_title(f"Comparaison à t = {t1:.2f}")
        except StopIteration:
            pass
        return line_hj, line_cons, line_u

    ani = animation.FuncAnimation(
        fig, update, interval=1, blit=True, frames=None, cache_frame_data=False
    )
    plt.show()

# ----------- Lancer l’animation ----------- #
if __name__ == "__main__":
    animate_comparison()
