#%%
import numpy as np
import matplotlib.pyplot as plt 


def exact(x):
    return np.exp(x)-np.exp(b) + (alpha-np.exp(a))*(x-b) + beta

#print(x)
#print(len(x))

def poisson1D(nint,f,opt_plot):

    a = 0
    b = 3
    alpha = -5
    beta = 3 
    
    h = (b-a)/nint
    x = np.arange(a,b+h,h)
    
    
    # Creation de la matrice A
    A = -2*np.identity(len(x)-1)
    b = [1]*(len(x)-2)
    np.fill_diagonal(A[1:],b)
    np.fill_diagonal(A[:,1:],b)
    A[0,0] = -3/2
    A[0,1] = 2
    A[0,2] = -1/2
    
    A = A*(1/h**2)
    #print(A.shape)
    
    # Creation du vecteur F
    F = [0]
    for i in range(1,len(x)-1):
        F.append(f(x[i]))
    #print(len(F))
    
    # Creation du vecteur Bc
    Bc = np.zeros(len(x)-1)
    Bc[0] = alpha/h
    Bc[-1] = -beta/h**2

    # Calcul de la solution 
    Uh = np.linalg.inv(A).dot(F+Bc)
    Uh = np.append(Uh,beta)
    #print(Uh)

    # Calcul de l'erreur
    Uex = np.array([exact(x) for x in x])
    
    E = Uh - Uex
    err = max(np.abs(E))

    if opt_plot == 1 :

        # Création du graphique
        plt.plot(x, Uh, marker='.') 
        plt.title("Solution numérique avec "+str(nint+1)+" points")
        plt.show()

    

    return Uh,err




# Solution approchée
#Uh, err = poisson1D(nint=10,f=np.exp,opt_plot=0)
#print("erreur:",err)

# Tracer le graphique en log-log
hvec = [10,20,40,80]
err_vec = []
for nint in hvec:
    err_vec.append(poisson1D(nint=nint,f=np.exp,opt_plot=0)[1])


print(len(err_vec))
print(len(hvec))
plt.loglog(hvec,err_vec)




    # %%
