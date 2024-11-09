#%%
import numpy as np
import matplotlib.pyplot as plt


def schema_chaleur2D(u0,m,p,T,CFL=1):
    dx = 1/(m+2)
    dy = 1/(p+2)
    dt = (dx*dy/2/(dx**2 + dy**2))*CFL

    
    lambda_x = dt/dx**2 
    lambda_y = dt/dy**2

    



    return




