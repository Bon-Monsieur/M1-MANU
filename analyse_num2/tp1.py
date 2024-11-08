#%%
import numpy as np
import matplotlib.pyplot as plt
import math

x = 1
y = 1

def u(x,y):
    return np.cos(x**2 + y**2)

def Lh(x,y,h):
    return (u(x+h,y)+u(x,y+h)-4*u(x,y)+u(x-h,y)+u(x,y-h))/h**2

def Laplacien_u(x,y):
    return -4*np.sin(x**2 + y**2)-(4*x+4*y)*(np.cos(x**2 + y**2))

h = [1e-1, 5e-2, 1e-2, 5e-3, 1e-3]  # tableau des h

tau_h = [np.abs(Lh(1,1,h)-Laplacien_u(1,1)) for h in h]
print(tau_h)

# Affiche en échelle logarithmique tau en fonction de h pour chaque méthode
plt.loglog(h,tau_h,label=r'$\tau_h$')
plt.loglog(h,[i**2 for i in h],label=r'$h^2$')
plt.legend()
plt.show()


# %%


def CoefDF(k, xbar, x):
    x = np.array(x)
    n = len(x)
    A = np.zeros((n, n))
    B = np.zeros((n, 1))
    h = min(x[1:n] - x[0:n-1])
    h2 = min(abs(x - xbar))
    if h2 > 0:
        h = min(h, h2)
    p = n - k
    for i in range(n):
        for j in range(n):
            A[i, j] = (x[j] - xbar) ** i / math.factorial(i)
    B[k] = 1
    coef = np.linalg.solve(A, B)
    coef = coef*h**k
    
    return coef


ptx = []
coefx = []
# Approximation du Laplacien avec 9 points
def Lh_9pt(x,y,h):
    xbar = x
    pt = np.array([xbar-2*h,xbar-h,xbar,xbar+h,xbar+2*h])
    l = [2*(coefx[i])*u(pt[i],y)/h**2 for i in range(len(pt))]
    return sum(l)


h = 0.1
k = 2
ptx = np.array([x-2*h,x-h,x,x+h,x+2*h])
coefx = CoefDF(k,x,ptx)
#print(coefx)

tau_h = []
H = [5e-1,1e-1, 5e-2, 1e-2, 5e-3]  # tableau des h
for h in H:
    tau_h.append(np.abs(Lh_9pt(1,1,h)-Laplacien_u(1,1)))


# Affiche en échelle logarithmique tau en fonction de h pour chaque méthode
plt.loglog(H,tau_h,label=r'$\tau_h$')
plt.loglog(H,[i**2 for i in H],label=r'$h^2$')
plt.loglog(H,[i**4 for i in H],label=r'$h^4$')
plt.legend()
plt.show()


# %%
