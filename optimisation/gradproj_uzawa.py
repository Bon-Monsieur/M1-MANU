#%%
import matplotlib.pyplot as plt 
import numpy as np
from scipy.linalg import hilbert
#%%

icase=1

if(icase==1):
    ############################################
    def func(ndim, x):
        alp1=0.1
        alp2=0.1
        cost = x[0]**2 + x[1]**2
        cons1 = -((x[0] - 1)**2 + x[1]**2 -1)
        cons2 = -((x[0] + 4)**2 + (x[1] + 3)**2 - 30)
        f=cost+alp1*abs(cons1)+alp2*abs(cons2)
    #penalisation: J(x) <- J(x) + sum alp_i |Ei(x)|
        return f
    ###########################################
    def funcp(ndim, x):
        rouzawa=-0.2  #va etre multiplier par rho de descente  xn+1 = xn -rho fp
        fp=[2*x[0] + 2*x[2]*(x[0] - 1) + 2*x[3]*(x[0] + 4),
            2*x[1] + 2*x[2]*x[1] + 2*x[3]*(x[1] + 3),
            rouzawa*(((x[0] - 1)**2 + x[1]**2 -1)),
            rouzawa*((x[0] + 4)**2 + (x[1] + 3)**2 - 30)
            ]
        return fp
############################################
if(icase==2):
    def func(ndim, x):   #J(x)=1/2 (Ax,x) - (b,x) + c
        ndimc=ndim-1
        xc=x[:ndimc]
        p=x[ndimc]
        A=hilbert(ndimc)
        xcible=np.ones((ndimc))
        b=A.dot(xcible)
        B=np.ones(ndimc)
        c=1
        Constraint=B.dot(x[:ndimc])-c
        f=0.5*(A.dot(xc)).dot(xc)-b.dot(xc)+p*Constraint
        return f
    ############################################
    def funcp(ndim, x):    
        rouzawa=-0.2  #va etre multiplier par rho de descente  xn+1 = xn -rho fp
        ndimc=ndim-1
        xc=x[:ndimc]
        p=x[ndimc]
        A=hilbert(ndimc)
        xcible=np.ones((ndimc))
        b=A.dot(xcible)
        B=np.ones(ndimc)
        c=1
        Constraint=(c-B.dot(xc))*rouzawa
        grad=A.dot(xc)-b-B.transpose().dot(p)
        fp=[]
        for i in range(ndimc):
            fp.append(grad[i])
        fp.append(Constraint)    
        return fp
############################################


nbgrad=10000
eps=1.e-6
epsdf=0.01
ndim=4
idf=0
ro0=0.01

ro=ro0
history=[]
historyg=[]
    
dfdx=np.zeros((ndim))
xmax=np.ones((ndim))*20
xmin=-np.ones((ndim))*20
x=np.ones((ndim))

  
dfdx=np.zeros((ndim))
d=dfdx

crit=1
itera=-1
while(itera<nbgrad and crit>eps):
    itera+=1
    
    dfdx0=dfdx
    
    if(idf==1):
        for i in range(0, ndim):
            x[i]=x[i]+epsdf
            fp=func(ndim, x)
            x[i]=x[i]-2*epsdf
            fm=func(ndim, x)
            x[i]=x[i]+epsdf
            dfdx[i]=(fp-fm)/(2*epsdf)
    elif(idf==0):
        dfdx=funcp(ndim,x)
                       
    gg=0
    for i in range(ndim):
        gg=gg+dfdx[i]**2
        x[i]-=ro*dfdx[i]
        x[i]=max(min(x[i], xmax[i]), xmin[i])
        
    f=func(ndim, x)
    history.append(f)
    historyg.append(gg)

####################################################
#two ways to define the step size
#incomplete linesearch 
#            ro1=3
#            beta=0.5        
#            for i in range(0, 10):
#                xtest=x+ro1*d
#                ftest=func(ndim,xtest)
#                if(ftest > f-ro1/2*gg):
#                    ro1=ro1*beta
#                ro=ro1        
#heuristic for ro tuning        
#        if (itera >2 and history[itera-1] > f):
#            ro=min(ro*1.25, 100*ro0)
#        else:
#            ro=max(ro*0.6, 0.01*ro0)
#####################################################

    # g1=dfdx[0]
    # g2=dfdx[1]
    # xnoj=np.sqrt(g1**2+g2**2)        
    # gc11 = 2 * x[0] - 2;
    # gc12 = 2 * x[1];
    # gc21 = 2 * x[0] + 8;
    # gc22 = 2 * x[1] + 6;
    # xnoc1=np.sqrt(gc11**2+gc12**2)
    # xnoc2=np.sqrt(gc21**2+gc22**2)
    # ps1=(gc11*g1+gc12*g2)/xnoc1
    # ps2=(gc11*g1+gc12*g2)/xnoc2
    # g1-=ps1*gc11/xnoc1+ps2*gc21/xnoc2
    # g2-=ps1*gc12/xnoc1+ps2*gc22/xnoc2
    # crit=abs(g1)+abs(g2)
  
#        if(abs(g1)+abs(g2)<eps):    #critere d'arret 

h1=abs(history[0])
hg1=abs(historyg[0])

for iter in range(itera+1):
    history[iter]=history[iter]/h1
    historyg[iter]=historyg[iter]/hg1

plt.plot(history, color='red', label='GD')
plt.legend()
plt.show()
   
print('iterations=',itera)
print('convergence criteria=',crit)
print('uzawa (x,p)=',x)
if(icase==1):
    print('target(x,p)= [0.16754469  0.55409219 -0.325321   -0.10518421]')
    print("C1:",(x[0] - 1)**2 + x[1]**2 -1)
    print("C2:",(x[0] + 4)**2 + (x[1] + 3)**2 - 30)

if(icase==2):
    ndimc=ndim-1
    B=np.ones(ndimc)
    c=1
    print("Constraint Bx-c=",B.dot(x[:ndimc])-c)
# %%
