#%%

import numpy as np
import matplotlib.pyplot as plt

#%%

a = 1
up_a = np.cos(1)

def u(x):
    return np.sin(x)

def Dp_u(x,h):
    return (u(x+h)-u(x))/h

def Dm_u(x,h):
    return (u(x)-u(x-h))/h

def D0_u(x,h):
    return (u(x+h)-u(x-h))/(2*h)

def D3_u(x,h):
    return (2*u(x+h)+3*u(x)-6*u(x-h)+u(x-2*h))/(6*h)

#%%
# 1)
h = [1e-1, 5e-2, 1e-2, 5e-3, 1e-3] 
order = [1,1,2,3]

T_Dp = [np.abs(Dp_u(a,t)-up_a) for t in h]
T_Dm = [np.abs(Dm_u(a,t)-up_a) for t in h]
T_D0 = [np.abs(D0_u(a,t)-up_a) for t in h]
T_D3 = [np.abs(D3_u(a,t)-up_a) for t in h]

C_Dp = [(Dp_u(a,t)-up_a)/t**order[0] for t in h]
C_Dm = [(Dm_u(a,t)-up_a)/t**order[1] for t in h]
C_D0 = [(D0_u(a,t)-up_a)/t**order[2] for t in h]
C_D3 = [(D3_u(a,t)-up_a)/t**order[3] for t in h]

print(T_Dp)
print(T_Dm)
print(T_D0)
print(T_D3)
print()
#print(C_Dp)
#print(C_Dm)
#print(C_D0)
#print(C_D3)


#%%
# 2)

plt.plot(h,T_Dp,marker='.')
plt.plot(h,T_D0,marker='.')
plt.plot(h,T_D3,marker='.')

# Toutes les méthodes converges, mais la première 
# est moins précise au début

# %%
# 3) 

plt.loglog(h,T_Dp,label='T_Dp')
plt.loglog(h,T_Dm,label='T_Dm')
plt.loglog(h,T_D0,label='T_D0')
plt.loglog(h,T_D3,label='T_D3')
plt.loglog(h,h,label='h')
plt.loglog(h,[i**2 for i in h],label=r'$h^2$')
plt.loglog(h,[i**3 for i in h],label=r'$h^3$')
plt.legend()
plt.show()


# %%
# 4)

p_Dp = [np.log(T_Dp[i]/T_Dp[i+1])/np.log(h[i]/h[i+1]) for i in range(len(h)-1)]
p_Dm = [np.log(T_Dm[i]/T_Dm[i+1])/np.log(h[i]/h[i+1]) for i in range(len(h)-1)]
p_D0 = [np.log(T_D0[i]/T_D0[i+1])/np.log(h[i]/h[i+1]) for i in range(len(h)-1)]
p_D3 = [np.log(T_D3[i]/T_D3[i+1])/np.log(h[i]/h[i+1]) for i in range(len(h)-1)]

print(p_Dp)
print(p_Dm)
print(p_D0)
print(p_D3)


# %%
