#%%
import numpy as np
import matplotlib.pyplot as plt


# Définition des variables demandées
L = 10
v = 1
T = 10


def chaleur_1Dimp(Nx,Nt,u0):

    deltax = L/Nx
    x = np.linspace(0,L,Nx+1)

    deltat = T/Nt
    t = np.linspace(0,T,Nt+1)

    U = np.zeros(shape=(Nx+1,Nt+1))

    # Définition des constantes nécessaires
    C1 = u0(0)
    C2 = u0(L)
    lmbda = v*deltat/deltax**2

    # Initialisation de la matrice U
    for i in range(Nt+1):
        U[0,i] = C1
        U[Nx,i] = C2
    U[1:-1,0] = [u0(xi) for xi in x[1:-1]]

    # Construction de la matrice de discrétisation
    A = np.identity(Nx-1)*(1+2*lmbda)
    b = [-lmbda]*(Nx-2)
    np.fill_diagonal(A[1:],b)
    np.fill_diagonal(A[:,1:],b)

    Ainv = np.linalg.inv(A)
    Bc = np.zeros(Nx-1)*lmbda
    Bc[0] = C1
    Bc[-1] = C2
     

    for i in range(Nt):
        Uh = U[1:-1,i]
        res = Ainv.dot((Uh+Bc))
        
        # Ajout de la solution au tableau U 
        U[1:-1,i+1] = res


    return U


def u0_1(x):
    return np.exp(-5*(x-L/2)**2)

def u0_2(x):
    return 1 if L/2 - 1 <= x <= L/2 + 1 else 0

def u0_3(x):
    return np.sin(np.pi*x/L)+np.sin(10*np.pi*x/L)


#%%

Nx = 100
Nt = 20
x = np.linspace(0,L,Nx+1)

U_1 = chaleur_1Dimp(Nx,Nt,u0_1)

for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_1[:,i])
    #plt.plot(x, U_1[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = $\exp(-5*(x-\frac{L}{2})^2)$')
    plt.legend()
plt.show()


U_2 = chaleur_1Dimp(Nx,Nt,u0_2)

for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_2[:,i])
    #plt.plot(x, U_2[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = 1 ou 0')
    plt.legend()
plt.show()

U_3 = chaleur_1Dimp(Nx,Nt,u0_3)

for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_3[:,i])
    #plt.plot(x, U_3[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = $\sin(\frac{\pi x}{L}) + \sin(\frac{10\pi*x}{L})$')
    plt.legend()
plt.show()

# %%
