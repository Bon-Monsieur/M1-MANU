import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ----------- Paramètres globaux ----------- #
a = -10
b = 10
nb_maille = 300
dx = (b - a) / nb_maille
T = 1e9
CFL = 0.5

x_milieu = np.linspace(a + dx/2, b - dx/2, nb_maille)

# ----------- Fonction u0(x) et rho0(x) ----------- #
def u0(x):
    return x*0.4  # Convexe, u_x entre 0 et 1

def rho0(x):
    return 0.4

# ----------- Hamiltonien et flux de Godunov ----------- #
def H(p):
    return p * (1 - p)

def H_prime(p):
    return 1 - 2 * p

def g_H(p_minus, p_plus):
    if p_minus <= p_plus:
        p_star = 0.5
        if p_minus <= p_star <= p_plus:
            return H(p_star)
        else:
            return min(H(p_minus), H(p_plus))
    else:
        return max(H(p_minus), H(p_plus))

vectorized_g_H = np.vectorize(g_H)

# ----------- Schéma Hamilton-Jacobi ----------- #
def schema_generator(nb_maille, u0, a, b, f, fp, cfl, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    it = 0
    t = 0

    Uh = np.array([u0((x[i] + x[i+1]) / 2.0) for i in range(len(x) - 1)])

    while t < T:
        Utemp = Uh.copy()

        du_left = (Utemp[1:-1] - Utemp[:-2]) / dx
        du_right = (Utemp[2:] - Utemp[1:-1]) / dx

        Cn = np.max(np.abs(fp(Utemp)))
        dt = cfl * dx / max(Cn, 1e-6)

        if T - t < dt:
            dt = T - t
        t += dt

        Uh[1:-1] -= dt * vectorized_g_H(du_left, du_right)
        Uh[0] = Utemp[0]
        Uh[-1] = Utemp[-1]

        if it % 10 == 0 or t + dt >= T:
            yield t, Uh.copy()

        it += 1

# ----------- Schéma conservation scalaire ----------- #
def conservation_law_solver(nb_maille, rho0, a, b, H, H_prime, cfl, T):
    m = nb_maille
    x = np.linspace(a, b, m + 1)
    dx = (b - a) / m
    x_center = (x[:-1] + x[1:]) / 2

    t = 0
    it = 0
    rho = np.array([rho0(xi) for xi in x_center])

    while t < T:
        rhotemp = rho.copy()

        vmax = np.max(np.abs(H_prime(rhotemp)))
        dt = cfl * dx / max(vmax, 1e-6)

        if t + dt > T:
            dt = T - t
        t += dt

        F_plus = vectorized_g_H(rhotemp[:-1], rhotemp[1:])
        rho[1:-1] -= dt / dx * (F_plus[1:] - F_plus[:-1])
        rho[0] = rhotemp[0]
        rho[-1] = rhotemp[-1]

        if it % 10 == 0 or t + dt >= T:
            yield t, rho.copy()

        it += 1

# ----------- Dérivée discrète centrée ----------- #
def discrete_derivative(Uh, dx):
    dUh = np.zeros_like(Uh)
    dUh[1:-1] = (Uh[2:] - Uh[:-2]) / (2 * dx)
    dUh[0] = (Uh[1] - Uh[0]) / dx
    dUh[-1] = (Uh[-1] - Uh[-2]) / dx
    return dUh

# ----------- Animation de la comparaison ----------- #
def animate_comparison():
    gen_hj = schema_generator(nb_maille, u0, a, b, H, H_prime, cfl=CFL, T=T)
    gen_cons = conservation_law_solver(nb_maille, rho0, a, b, H, H_prime, cfl=CFL, T=T)

    fig, ax = plt.subplots()
    line_hj, = ax.plot([], [], 'b-', label=r"$\partial_x u$ (HJ)")
    line_cons, = ax.plot([], [], 'r--', label=r"$\rho$ (conservation)")
    ax.set_xlim(a , b )
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("Valeur")
    ax.set_title(r"Comparaison : dérivée de $u$ vs $\rho$")
    ax.legend()

    def update(frame):
        try:
            t1, Uh = next(gen_hj)
            t2, rho = next(gen_cons)
            rho_from_HJ = discrete_derivative(Uh, dx)

            line_hj.set_data(x_milieu, rho_from_HJ)
            line_cons.set_data(x_milieu, rho)
            ax.set_title(f"Comparaison à t = {t1:.2f}")
        except StopIteration:
            pass
        return line_hj, line_cons

    ani = animation.FuncAnimation(
        fig, update, interval=10, blit=True, frames=None, cache_frame_data=False
    )
    plt.show()

# ----------- Lancer l’animation ----------- #
if __name__ == "__main__":
    animate_comparison()
