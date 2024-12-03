#%%
import numpy as np
import matplotlib.pyplot as plt



def schema_VF(nb_maille,u0,a,b,f,fp,gamma,cfl=0.5,T=1):

    m = nb_maille
    x = np.linspace(a,b,m+1)
    dx = (b-a)/m
    

    Uh = u0(x)
    #print(Uh[0])  #  len(Uh) = m
    #plt.plot(x[:-1],Uh)
    #print(len(Uh)) 
    
    t = 0
    it = 0

    def flux(um,up):
        return 1/2*(f(um)+f(up)) - gamma(um,up,f,fp,Uh)/2 * (up - um)

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
        

    # Vectorisation de la fonction flux
    vectorized_flux = np.vectorize(flux)

    while t < T and it<10**3:
        it += 1

        # Calcul du nouveau pas de temps
        Cn = max([np.abs(fp(ui)) for ui in Uh])
        dt =  cfl * dx/Cn
        #if it == 1 :
            #print(Cn)
        #print(Cn)
        
        # Derniere iteration
        if T - t < dt:
            dt = T - t
        t += dt

        # Sauvegarde des valeurs pour les bords 
        m1,ml2 = Uh[1], Uh[-2]
        m0,ml = Uh[0], Uh[-1]

        # si U0 periodique 
        '''
        Uh[0] = m0 - dt / dx * (flux(m0,m1) - flux(ml,m0))
        Uh[-1] = ml - dt / dx * (flux(ml,m0) - flux(ml2,ml))
        '''

        # Si U0 pas périodique (cours)
        Uh[0] = m0 - dt / dx * (flux(m0,m1) - flux(solution_exacte_cours(a,t),m1))
        Uh[-1] = ml - dt / dx * (flux(ml,solution_exacte_cours(b,t)) - flux(ml2,ml))

        # Formule VF mailles interieurs ?
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


def u0_td(x):
    return [np.sin(2*np.pi*(x[i]+x[i+1])/2) for i in range(len(x)-1)]

def u0_cours(x):
    res = []
    for i in range(len(x)-1):
        if (x[i]+x[i+1])/2 <0.3 :
            res.append(0)
        elif 0.3 < (x[i]+x[i+1])/2 <0.7 :
            res.append(-1)
        else:
            res.append(1/2)
    return res

def solution_exacte_cours(x,t=2):
    t_etoile = 0.8
    res = []
    if (t<t_etoile):
        for i in range(len(x)-1):
            if x[i] <0.3-t/2 :
                res.append(0)
            elif 0.3-t/2 < x[i] <0.7-t :
                res.append(-1)
            elif -1 <= (x[i]-0.7)/t <= 1/2:
                res.append((x[i]-0.7)/t)
            else:
                res.append(1/2)
    else:
        for i in range(len(x)-1):
            if x[i] <-np.sqrt(0.8*t) + 0.7 :
                res.append(0)
            elif -np.sqrt(0.8*t) + 0.7 <= x[i] <= 0.7 + t/2:
                res.append((x[i]-0.7)/t)
            else:
                res.append(1/2)
    return res

def gamma_LFg(um,up,f,fp,Uh):
    return max([np.abs(fp(ui)) for ui in Uh])

def gamma_LFl(um,up,f,fp,Uh):
    return max([np.abs(fp(um)),np.abs(fp(up))])

def gamma_MurmanR(um,up,f,fp,Uh):
    if um != up:
        return np.abs((f(up)-f(um))/(up-um))
    else:
        return np.abs(fp(up))




a = -1
b = 1
nb_maille = 100
T = 3
x = np.linspace(a, b, nb_maille+1)
dx = (b-a)/nb_maille
x_milieu = np.linspace(a+dx/2,b-dx/2,nb_maille)

Uh_LFg = schema_VF(nb_maille, u0_cours, a, b, f, fp, gamma_LFg, T=T)
Uh_LFl = schema_VF(nb_maille, u0_cours, a, b, f, fp, gamma_LFl, T=T)
Uh_MR = schema_VF(nb_maille, u0_cours, a, b, f, fp, gamma_MurmanR, T=T)
print(Uh_MR[0])
plt.plot(x_milieu, Uh_LFg, label='LFg')
plt.plot(x_milieu, Uh_LFl, label='LFl')
plt.plot(x_milieu, Uh_MR, label='Murman-Roe')
plt.plot(x_milieu, solution_exacte_cours(x,T), label='Solution exacte', linestyle='--')
#plt.plot(x_milieu, u0_cours(x), label='initiale', linestyle='--')
plt.legend()
plt.show()


# %%
