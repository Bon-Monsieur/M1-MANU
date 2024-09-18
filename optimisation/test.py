#%%
import numpy as np
import matplotlib.pyplot as plt

#%%
#main program

iteration = 100

def f(v):
    x,y = v
    return 0.5*(x**2+3*y**2) #+ 3*x*y +1

def grad_f(v):
    x,y =v
    g0 = x #+3*y
    g1 = 3*y #+3*x
    res = np.array([g0,g1]) 

x =  np.array([1,1])
def descente(grad_f, x_init, maxiter, epsilon,func,rho): #Methode de descente
    x = x_init
    results = [x]
    values = [func(x)]
    for i in range(1, maxiter + 1):
        g = grad_f(x)
        if np.linalg.norm(g) <= epsilon:
            break   
        else:
            x = x-rho*g
            results.append(x)
            values.append(func(x))
    return results,values


print(descente(grad_f=grad_f,x_init=x,maxiter=iteration,epsilon=0.001,func=f,rho=0.01)[0][-1])


iter = [i for i in range(iteration)]
norm



#Define constants
#store convergence histories

#define admissible space

#initialization 

#loop over descent iterations


#calculate gradient by explicit expression and by finite differences


#calculate norm of gradient

#calculate new iterate xn+1 and enforce admissible bounds

#calculate new functional J(xn+1)

#store convergence results

#introduce stopping criteria

#redefine descent step size rho


#plot convergence results relative to first iteration values versus iterations
#add comprehensible legends 
#




# %%
