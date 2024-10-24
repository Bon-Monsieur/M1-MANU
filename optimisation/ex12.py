#%%
import numpy as np
import matplotlib.pyplot as plt

alpha1 = 1


def J(v):
    x1,x2,x3 = v
    return x1**2 -4*x1 - x1*x2 + x1*x3 + x2*x3

def h1(v):
    x1,x2,x3 = v
    return x1+x2+x3-1

def Jt(v):
    return J(v) + alpha*np.abs(h1(v))

tildJ_alpha = lambda alphas: (lambda x: J(x) + np.sum([a * np.abs(ei) for (a, ei) in zip(alphas, E(x))]))

def finite_difference_gradient(f, x, h=1e-5):

    x = np.array(x, dtype=float)  # convertir x en array numpy pour faciliter la manipulation
    grad = np.zeros_like(x)  # initialiser le vecteur gradient avec des zéros
    
    # Calcul du gradient par la méthode des différences finies
    for i in range(len(x)):
        x_forward = np.copy(x)
        x_forward[i] += h  # incrémente la ième composante de h
        
        x_backward = np.copy(x)
        x_backward[i] -= h  # décrémente la ième composante de h
        
        # Approximation de la dérivée partielle par différence centrée
        grad[i] = (f(x_forward) - f(x_backward)) / (2 )
    
    return grad


# Descente de gradient avec grad_Jt
def descente(fun, x_init, gamma, maxiter, epsilon): 
    x = x_init
    results = [x]
    iter = 1

    while(iter<maxiter and np.linalg.norm(finite_difference_gradient(fun,x)) >= epsilon):
        g = finite_difference_gradient(fun,x)
        x = x-gamma*g
        results.append(x)
        iter +=1
    return results

def Penalisation(func, x, h, rho, max_iter):
    return descente(func, x, h, rho, max_iter)


ndim = 3 
Alphas = np.linspace(0, 30, num=100)

n = 3
x0 = np.ones(n)
rho = 1e-3
max_iter = 1000

X_alphas = np.array([Penalisation(tildJ_alpha([alpha]), x0, 1e-1, rho, max_iter) for alpha in Alphas])



E_alphas = [h1(x) for x in X_alphas]
J_alphas = [J(x) for x in X_alphas]
# plt.plot(E_alphas, J_alphas, 'o')
plt.plot(Alphas, J_alphas, 'o',)
# plt.scatter(E_alphas[0], J_alphas[0], color='red')
plt.scatter(Alphas[0], J_alphas[0], color='red', s=30 )
# plt.xlabel("E alpha")
plt.xlabel("Alpha")
plt.ylabel("J alpha")
plt.tight_layout()
plt.legend()
# plt.figure()
plt.plot(Alphas, [np.linalg.norm(x-np.array([-1,1,-1])) for x in X_alphas], 'o',label="dist to opt")
plt.xlabel("alpha")
plt.ylabel("dist to J theoretical min")
plt.tight_layout()
plt.legend()



# %%
import numpy as np
import matplotlib.pyplot as plt



def FDC(func, x, h):
    H = np.eye(x.size) * h
    return np.array([(func(x + hi) - func(x - hi)) / 2 for hi in H[:,]])


def FD_GD(func, x, h, rho, max_iter):
    iter_count = 0
    while np.linalg.norm(FDC(func, x, h)) > rho and iter_count < max_iter:
        # Calculate new iterate xn+1 using gradient descent step
        x = x - rho * FDC(func, x, h)
        iter_count += 1
    return x


E = lambda x: [x[0] + x[1] + x[2] - 1]


J = lambda x: x[0] ** 2 - 4 * x[0] - x[0] * x[1] + x[0] * x[2] + x[1] * x[2]

tildJ_alpha = lambda alphas: (lambda x: J(x) + np.sum([a * np.abs(ei) for (a, ei) in zip(alphas, E(x))]))

def Penalisation(func, x, h, rho, max_iter):
    return FD_GD(func, x, h, rho, max_iter)

n = 3
x0 = np.ones(n)
rho = 1e-3
max_iter = 1000
Alphas = np.linspace(0, 30, num=100)
X_alphas = np.array([Penalisation(tildJ_alpha([alpha]), x0, 1e-1, rho, max_iter) for alpha in Alphas])
# print(X_alphas)
# %%
print(len(X_alphas))
E_alphas = [E(x)[0] for x in X_alphas]
J_alphas = [J(x) for x in X_alphas]
# plt.plot(E_alphas, J_alphas, 'o')
plt.plot(Alphas, J_alphas, 'o',)
# plt.scatter(E_alphas[0], J_alphas[0], color='red')
plt.scatter(Alphas[0], J_alphas[0], color='red', s=30 )
# plt.xlabel("E alpha")
plt.xlabel("Alpha")
plt.ylabel("J alpha")
plt.tight_layout()
plt.legend()
# plt.figure()
plt.plot(Alphas, [np.linalg.norm(x-np.array([-1,1,-1])) for x in X_alphas], 'o',label="dist to opt")
plt.xlabel("alpha")
plt.ylabel("dist to J theoretical min")
plt.tight_layout()
plt.legend()
# %%
