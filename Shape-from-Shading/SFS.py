import numpy as np
import matplotlib.pyplot as plt

nb_pt = 21
x = np.linspace(0,1,nb_pt)
y = np.linspace(0,1,nb_pt)
X,Y = np.meshgrid(x,y)
Dx = x[1]-x[0]
Dy = y[1]-y[0]

Dt = Dx*Dy/np.sqrt(Dx**2+Dy**2)

def I(v):
    x,y=v
    return 1 / np.sqrt(1 + (16 * y * (1 - y) * (1 - 2 * x))**2 + (16 * x * (1 - x) * (1 - 2 * y))**2)


def n(v):
    return np.sqrt(1/I(v)**2 - 1)

def Dxp(U,i,j):
    return (U[i+1,j]-U[i,j])/Dx

def Dxm(U,i,j):
    return (U[i,j]-U[i-1,j])/Dx

def Dyp(U,i,j):
    return (U[i,j+1]-U[i,j])/Dy

def Dym(U,i,j):
    return (U[i,j]-U[i,j-1])/Dy
     
def g(i,j,a,b,c,d):
    return np.sqrt(max(max(a,0),max(-b,0))**2+max(max(c,0),max(-d,0))**2) - n((x[i],y[j]))


def G(U,i,j):
    return g(i,j,Dxm(U,i,j),Dxp(U,i,j),Dym(U,i,j),Dyp(U,i,j))



Un = np.full((nb_pt,nb_pt), 0.0) #U0 == 0 
Up1= np.full((nb_pt,nb_pt), 0.0)


for k in range(200):
    Un = Up1.copy()
    Un[10,10]=1
    for i in range(1, nb_pt - 1):  # Assurez-vous de ne pas dépasser les limites
        for j in range(1, nb_pt - 1):  # Assurez-vous de ne pas dépasser les limites
            if i == 0 or i == nb_pt - 1 or j == 0 or j == nb_pt - 1:
                # Si on est sur un bord, on ne met pas à jour
                continue
            Up1[i, j] = Un[i, j] - Dt * G(Un, i, j)


Up1[10,10]=1

# Tracé de Uh en 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Up1, cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Uh')
ax.set_title('Tracé de Uh en 3D')

plt.show()
