import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def schema_VF(nb_maille,u0,a,b,f,fp,cfl=0.5,T=1,convexe=1,Nt_print_max=10):
    def F(t):
        return 0 if 30<t<50 or 100<t<120 or 160<t<200 else 0.55

        
    m = nb_maille
    x = np.linspace(a,b,m+1)
    dx = (b-a)/m
    
    # Initialisation 
    # Uh contient les valeurs des mailles 
    Uh = [u0((x[i]+x[i+1])/2.0) for i in range(len(x)-1)]
    
    t = 0
    it = 0

    # Definition du flux
    def flux(um,up):
        return 0.5*(f(um)+f(up)) -0.5*(up - um)
    vectorized_flux = np.vectorize(flux)

    Uh_history = [(t, Uh.copy())]
    i_centre = len(Uh) // 2 - 25

    while t < T:
        it += 1
        
        # Calcul du nouveau pas de temps
        if convexe == 1:
            Cn = max([np.abs(fp(ui)) for ui in Uh])
        if convexe != 1:
            Cn = 2.34
        dt =  cfl * dx/Cn
        
        # Derniere iteration
        if T - t < dt:
            dt = T - t
        t += dt

        Utemp = Uh.copy()
        
        Uh[0] = Utemp[0] - dt/dx *(flux(Utemp[0],Utemp[1]) - flux(0.55,Utemp[0]))  # Entrée de la route
        Uh[-1] = Utemp[-1] - dt/dx * (flux(Utemp[-1],0.0) - flux(Utemp[-2],Utemp[-1]))  # Sortie de la route
        
        
        Uh[1:-1] = (
            Uh[1:-1] 
            - dt/dx*(vectorized_flux(Uh[1:-1],Uh[2:])-vectorized_flux(Uh[:-2],Uh[1:-1]))
        )
        Uh[i_centre] = Utemp[i_centre] - dt / dx * (
                    flux(Utemp[i_centre], Utemp[i_centre+1]) - min(flux(Utemp[i_centre-1], Utemp[i_centre]),F(t))  # flux sortant = 0
                )
        Uh[i_centre-1] = Utemp[i_centre-1] - dt / dx * (
                    min(F(t),flux(Utemp[i_centre-1], Utemp[i_centre])) -  flux(Utemp[i_centre-2], Utemp[i_centre-1]) # flux entrant = 0
                )

        if it % ((T//dt)//Nt_print_max) == 0:
            Uh_history.append((t, Uh.copy()))   
    # End while 
    print(it)
    return Uh, Uh_history


def H(rho):
    return rho*(1-rho)

def Hp(rho):
    return 1 - 2*rho

def u0(x):
    return 0.55




# Def variables
a = -5
b = 5
nb_maille = 100
T = 250

# Def maillage
x = np.linspace(a, b, nb_maille+1)
dx = (b-a)/nb_maille
x_milieu = np.linspace(a+dx/2,b-dx/2,nb_maille)

Uh_final, Uh_history = schema_VF(
    nb_maille, u0, a, b, f=H, fp=Hp,
    cfl=0.25, T=T, convexe=1, Nt_print_max=200
)



def animate_solution(Uh_history, a, b, nb_maille):
    # Maillage centré
    dx = (b - a) / nb_maille
    x_milieu = np.linspace(a + dx/2, b - dx/2, nb_maille)

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(a, b)
    ax.set_ylim(0, 1)  # Adapter selon le problème
    ax.set_xlabel('x')
    ax.set_ylabel(r'$\rho(x,t)$')

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        t, Uh = Uh_history[frame]
        line.set_data(x_milieu, Uh)
        ax.set_title(f"Densité de voiture à t = {t:.2f}")
        return line,

    ani = animation.FuncAnimation(
        fig, update, frames=len(Uh_history),
        init_func=init, blit=False, interval=100
    )

    plt.show()
    return ani

animate_solution(Uh_history, a, b, nb_maille)