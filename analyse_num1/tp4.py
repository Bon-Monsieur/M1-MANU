#%%
import numpy as np
import matplotlib.pyplot as plt


# Définition des variables demandées
L = 10
v = 1
T = 30


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
    Bc = np.zeros(Nx-1)
    Bc[0] = C1*lmbda
    Bc[-1] = C2*lmbda
     

    for i in range(Nt):
        Uh = U[1:-1,i]
        res = Ainv.dot((Uh+Bc))
        
        # Ajout de la solution au tableau U 
        U[1:-1,i+1] = res


    return U

# Définition des différents u0 que l'on va utiliser
def u0_1(x):
    return np.exp(-5*(x-L/2)**2)

def u0_2(x):
    return 1 if L/2 - 1 <= x <= L/2 + 1 else 0

def u0_3(x):
    return np.sin(np.pi*x/L)+np.sin(10*np.pi*x/L)


#%%

# Affichage des convergences pour les 3 u0 
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

def chaleur_1Dexp(Nx,Nt,u0,CFL=0.05):

    deltax = L/Nx
    x = np.linspace(0,L,Nx+1)

    deltat = CFL*deltax**2/2/v
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
    A = np.identity(Nx-1)*(1-2*lmbda)
    b = [lmbda]*(Nx-2)
    np.fill_diagonal(A[1:],b)
    np.fill_diagonal(A[:,1:],b)

    Bc = np.zeros(Nx-1)
    Bc[0] = C1*lmbda
    Bc[-1] = C2*lmbda
     

    for i in range(Nt):
        Uh = U[1:-1,i]
        res = A.dot((Uh+Bc))
        
        # Ajout de la solution au tableau U 
        U[1:-1,i+1] = res
    
    return U


#%%
Nx = 15
Nt = 10
x = np.linspace(0,L,Nx+1)

U_1 = chaleur_1Dexp(Nx,Nt,u0_1,0.5)
for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_1[:,i])
    #plt.plot(x, U_1[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = $\exp(-5*(x-\frac{L}{2})^2)$')
    plt.legend()
plt.show()


U_2 = chaleur_1Dexp(Nx,Nt,u0_2,0.5)
for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_2[:,i])
    #plt.plot(x, U_2[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = 1 ou 0')
    plt.legend()
plt.show()

U_3 = chaleur_1Dexp(Nx,Nt,u0_3,0.5)
for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_3[:,i])
    #plt.plot(x, U_3[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = $\sin(\frac{\pi x}{L}) + \sin(\frac{10\pi*x}{L})$')
    plt.legend()
plt.show()

# %%
def chaleur_1DCN(Nx,Nt,u0):

    deltax = L/Nx
    x = np.linspace(0,L,Nx+1)

    deltat = T/Nt
    t = np.linspace(0,T,Nt+1)

    U = np.zeros(shape=(Nx+1,Nt+1))

    # Définition des constantes nécessaires
    C1 = u0(0)
    C2 = u0(L)
    lmbda = v*deltat/deltax**2/2

    # Initialisation de la matrice U
    for i in range(Nt+1):
        U[0,i] = C1
        U[Nx,i] = C2
    U[1:-1,0] = [u0(xi) for xi in x[1:-1]]

    # Construction de la matrice de discrétisation à gauche
    A1 = np.identity(Nx-1)*(1+2*lmbda)
    b1 = [-lmbda]*(Nx-2)
    np.fill_diagonal(A1[1:],b1)
    np.fill_diagonal(A1[:,1:],b1)
    A1inv = np.linalg.inv(A1)

    # Construction de la matrice de discrétisation à droite
    A2 = np.identity(Nx-1)*(1-2*lmbda)
    b2 = [lmbda]*(Nx-2)
    np.fill_diagonal(A2[1:],b2)
    np.fill_diagonal(A2[:,1:],b2)

    Bc = np.zeros(Nx-1)
    Bc[0] = 2*C1*lmbda
    Bc[-1] = 2*C2*lmbda
     

    for i in range(Nt):
        Uh = U[1:-1,i]
        res = A1inv.dot((A2.dot(Uh))+Bc)
        
        # Ajout de la solution au tableau U 
        U[1:-1,i+1] = res
    
    return U

#%%

Nx = 20
Nt = 13
x = np.linspace(0,L,Nx+1)

U_1 = chaleur_1DCN(Nx,Nt,u0_1)
for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_1[:,i])
    #plt.plot(x, U_1[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = $\exp(-5*(x-\frac{L}{2})^2)$')
    plt.legend()
plt.show()


U_2 = chaleur_1DCN(Nx,Nt,u0_2)
for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_2[:,i])
    #plt.plot(x, U_2[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = 1 ou 0')
    plt.legend()
plt.show()

U_3 = chaleur_1DCN(Nx,Nt,u0_3)
for i in range(Nt+1):
    t_val = i * T / Nt
    plt.plot(x, U_3[:,i])
    #plt.plot(x, U_3[:,i], label=f't={t_val:.2f}')
    plt.title(r'Solution avec $u_0$ = $\sin(\frac{\pi x}{L}) + \sin(\frac{10\pi*x}{L})$')
    plt.legend()
plt.show()
# %%
