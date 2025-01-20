#%%
import numpy as np
import matplotlib.pyplot as plt

c = 1
v = 0.1

def u0(X):
    a = np.array([np.sin(2*np.pi*x) for x in X[:-1]])
    a = np.append(a,a[0])
    #print(a)
    return a

def u_exacte(x,t) :
    return np.exp(-4*np.pi**2*v*t)*np.sin(2*np.pi*(x-c*t))

def schema(nb_pts,T):

    dx = 2/(nb_pts - 1)
    dt = 1/2*dx**2/v
    x = np.linspace(0, 2.0, nb_pts)
    t = 0
    it = 0
    
    l1 = c*dt/dx
    l2 = v*dt/dx**2
    
    
    
    U0 = u0(x) # Initialisation au temps t =0
    
    Uh = U0
    Uold = Uh
    

    while t < T:
        it +=1

        if t+dt>T:
            dt = T-t
            l1 = c*dt/dx
            l2 = v*dt/dx**2
        t += dt

        Uold = Uh
        
        Uh[1:-1] = (1+l1-2*l2)*Uold[1:-1] + (-l1+l2)*Uold[2:] +l2*Uold[:-2]

        Uh[0] = Uold[0]*(1+l1-2*l2)+ Uold[1]*(-l1+l2)+l2*Uold[-2] # U-1 = U[-2] car "U[-1]=U[0]"
        Uh[-1] = Uh[0]

    return Uh

nb_points = 50
x = np.linspace(0,2.0,nb_points)

T = 1

u_h = schema(nb_points,T=T)
u_ex = np.array([u_exacte(xi,T) for xi in x])
plt.plot(x,u_h,label='uh')
plt.plot(x,u_ex,label='u_ex')

plt.legend()
plt.show()

# %%
# Calcul de l'erreur

erreur = u_h-u_ex
print("T = 0.5")
print("erreur norme infinie",np.linalg.norm(erreur,np.inf))
print("erreur norme 1",np.linalg.norm(erreur,1))
print("erreur norme 2",np.linalg.norm(erreur,2))


# %%
T = 0.5
X1 = np.linspace(0,2.0,25)
X2 = np.linspace(0,2.0,50)
X3 = np.linspace(0,2.0,100)
X4 = np.linspace(0,2.0,200)
X5 = np.linspace(0,2.0,400)

Uh1 = schema(25,T)
Uh2 = schema(50,T)
Uh3 = schema(100,T)
Uh4 = schema(200,T)
Uh5 = schema(400,T)
#U_ex2 = [u_exacte(xi,0.5) for xi in X5]

plt.loglog(X1,Uh1)
plt.loglog(X2,Uh2)
plt.loglog(X3,Uh3)
plt.loglog(X4,Uh4)
plt.loglog(X5,Uh5)
#plt.loglog(X5,U_ex2)

plt.legend()
plt.show()
# %%
