#%%
import numpy as np
import matplotlib.pyplot as plt



def schema_VF(nb_maille,u0,a,b,f,fp,schema,cfl=0.5,T=1,periodique=0):

    m = nb_maille
    x = np.linspace(a,b,m+1)
    dx = (b-a)/m
    
    # Initialisation 
    # Uh contient les valeurs des mailles 
    Uh = [u0((x[i]+x[i+1])/2) for i in range(len(x)-1)]
    
    t = 0
    it = 0

    # Adapter le gamma en fonction du schema demande
    if schema == "LFg":
        gamma = lambda um, up : max([np.abs(fp(ui)) for ui in Uh])
    if schema == "LFl":
        gamma = lambda um, up: max([np.abs(fp(um)),np.abs(fp(up))])
    if schema == "MR":
        gamma = lambda um, up: np.abs((f(up)-f(um))/(up-um)) if um != up else np.abs(fp(up))

    # Definition du flux
    def flux(um,up):
        return 1/2*(f(um)+f(up)) - gamma(um,up)/2 * (up - um)


    # Vectorisation de la fonction flux afin de pouvoir donner des tableaux à ma fonction en param
    vectorized_flux = np.vectorize(flux)


    while t < T and it<10**3:
        it += 1
        
        # Calcul du nouveau pas de temps
        Cn = max([np.abs(fp(ui)) for ui in Uh])
        #Cn = 2.34
        dt =  cfl * dx/Cn
        
        # Derniere iteration
        if T - t < dt:
            dt = T - t
        t += dt


        # Sauvegarde des valeurs pour le calcul de la solution aux bords
        m1,ml2 = Uh[1], Uh[-2]
        m0,ml = Uh[0], Uh[-1]

        # Calcul des bords si u0 periodique 
        if periodique==1:
            Uh[0] = m0 - dt / dx * (flux(m0,m1) - flux(ml,m0))
            Uh[-1] = ml - dt / dx * (flux(ml,m0) - flux(ml2,ml))

        # Calcul des bords si u0 n'est pas périodique
        if periodique!=1:
            Uh[0] = m0 - dt / dx * (flux(m0,m1) - flux(solution_exacte_cours(a,t),m1))
            Uh[-1] = ml - dt / dx * (flux(ml,solution_exacte_cours(b,t)) - flux(ml2,ml))
        
        

        # Formule VF mailles interieures 
        Uh[1:-1] = (
            Uh[1:-1] 
            - dt/dx*(vectorized_flux(Uh[1:-1],Uh[2:])-vectorized_flux(Uh[:-2],Uh[1:-1]))
        )
    
    # End while 
    return Uh


# BURGERS
def f(u):
    return 1/2*u**2

def fp(u):
    return u

# Les u0 utilisables
def u0_td(x):
    return np.sin(2*np.pi*x)

def u0_cours(x):
    if x <0.3 :
        return 0
    elif 0.3 < x <0.7 :
        return -1
    else:
        return 1/2

def u0_nc(x):
    if -1/2<x<0:
        return 1
    else:
        return 0
    

def solution_exacte_cours(x,t):
        t_etoile = 0.8
        if (t<t_etoile):
            if x <0.3-t/2 :
                return 0
            elif 0.3-t/2 < x <0.7-t :
                return -1
            elif -1 <= (x-0.7)/t <= 1/2:
                return (x-0.7)/t
            else:
                return 1/2
        else:
            if x <-np.sqrt(0.8*t) + 0.7 :
                return 0
            elif -np.sqrt(0.8*t) + 0.7 <= x <= 0.7 + t/2:
                return (x-0.7)/t
            else:
                return 1/2

def test(x,t):
    return 1/2/np.pi*np.arccos(x-1/2/np.pi/t)


# Pour le flux non convexe
def fnc(u):
    return 4*u**2/(4*u**2+(1-u)**2)

def fncp(u):
    return (8*u*(4*u**2+(1-u)**2) - 4*u**2*(8*u-2*(1-u)))/(4*u**2+(1-u)**2)**2


# Newton
def Newton(x0,x,t, tol=1e-3, max_iter=100):
    
    tab = [x0] # Stocke les xk 

    # Fonction dont il faut trouver le 0
    def g(X):
        return  2*np.pi*np.cos(2*np.pi*X)*t + X - x

    def gp(X):
        return -4*np.pi**2*np.sin(2*np.pi*X)*t + 1 

    xk = x0
    for i in range(max_iter):
        gx = g(xk)
        gpx = gp(xk)
        #print(gp(x))
        if np.abs(g(tab[i-1]) - g(tab[i])) < tol and i>1:  # Critère de convergence
            
            return xk
        
        if gpx == 0:  # Vérifie si la dérivée est nulle
            raise ValueError("La dérivée s'annule, la méthode de Newton ne peut pas continuer.")
        
        xk = xk - gx / gpx  # Mise à jour de x selon la méthode de Newton
        tab.append(xk.copy())
    raise ValueError("La méthode de Newton n'a pas convergé après le nombre maximal d'itérations.")




#%%
# Variables 
a = 0
b = 1
nb_maille = 100
T = 1/2/np.pi *0.9
period = 1 # 1 if u0 periodique else 0
u0 = u0_td

# Def du maillage
x = np.linspace(a, b, nb_maille+1)
dx = (b-a)/nb_maille
x_milieu = np.linspace(a+dx/2,b-dx/2,nb_maille)


Uh_LFg = schema_VF(nb_maille, u0, a, b, f, fp, "LFg", T=T,periodique=period)
Uh_LFl = schema_VF(nb_maille, u0, a, b, f, fp, "LFl", T=T,periodique=period)
Uh_MR = schema_VF(nb_maille, u0, a, b, f, fp, "MR", T=T,periodique=period)

plt.plot(x_milieu, Uh_LFg, label='LFg')
plt.plot(x_milieu, Uh_LFl, label='LFl')
plt.plot(x_milieu, Uh_MR, label='MR')

plt.plot(x_milieu, [u0_td(xi) for xi in x_milieu], label='initiale',linestyle='--')
#plt.plot(x_milieu, [u0_cours(xi) for xi in x_milieu], label='initiale', linestyle=':')

X = [Newton(0.8,xi,T) for xi in x_milieu]
print(X)
print(x_milieu)
plt.plot(x_milieu, [u0_td(xi) for xi in X], label='exacte')
#plt.plot(x_milieu, [solution_exacte_cours(xi,T) for xi in x_milieu], label='Solution exacte', linestyle='--')

plt.legend()
plt.show()

#plt.plot(x_milieu, [u0_td(test(xi,T)) for xi in x_milieu], label='initiale')



# %%
# Def variables
a = -1
b = 1
nb_maille = 10
T = 0.4
period = 1 # 1 if u0 periodique else 0
u0 = u0_nc

# Def maillage
x = np.linspace(a, b, nb_maille+1)
dx = (b-a)/nb_maille
x_milieu = np.linspace(a+dx/2,b-dx/2,nb_maille)


Uh_LFg = schema_VF(nb_maille, u0, a, b, fnc, fncp, "LFg", T=T,periodique=period)
Uh_LFl = schema_VF(nb_maille, u0, a, b, fnc, fncp, "LFl", T=T,periodique=period)
Uh_MR = schema_VF(nb_maille, u0, a, b, fnc, fncp, "MR", T=T,periodique=period)

plt.plot(x_milieu, Uh_LFg, label='LFg')
plt.plot(x_milieu, Uh_LFl, label='LFl')
plt.plot(x_milieu, Uh_MR, label='MR')

# Afficher solution prof
fichier = 'buckley.dat'
data = np.loadtxt(fichier)

# Tracer les points
# Extraire les colonnes
x = data[:, 0]  # Colonne de gauche (abscisses)
y = data[:, 1]  # Colonne de droite (ordonnées)
plt.plot(x, y, '--',label='sol exacte')
plt.legend()
plt.show()


# %%
