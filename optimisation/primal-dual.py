#%%
import numpy as np

n = 2

def hilbert_matrix(n):
    """Renvoie une matrice de Hilbert de taille n x n."""
    H = np.zeros((n, n))  # Créer une matrice n x n remplie de zéros
    for i in range(n):
        for j in range(n):
            H[i, j] = 1 / (i + j + 1)  # Les indices commencent à 0, donc ajouter 1
    return H

A = hilbert_matrix(n)
B = np.ones(n)
c = 1
b = np.dot(A,np.ones(n))

C = np.dot(np.dot(B,np.linalg.inv(A)),b)-c
D = np.dot(np.dot(B,np.linalg.inv(A)),B.T)


p = C/D
print(p)

E = b-B.T*p
x = np.dot(np.linalg.inv(A),E)
print(x)
#print(np.dot(B,x))
# %%

# Exemple avec J(x, y) = 1/2*(Ax,x) sous la contrainte affine x + y = 1.

R = 0.02
ri = np.array([])

A = np.array([[2,0],[0,4]])
B = np.array([1,1])
c = 1

b = np.array([0,0])

C = np.dot(np.dot(B,np.linalg.inv(A)),B)
D = np.dot(np.dot(B,np.linalg.inv(A)),b)-c

p = D/C
#print(p)

E = b-B*p
x = np.linalg.solve(A,E)
print(x)
#print(np.dot(B,x))

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Lire le fichier texte en spécifiant le séparateur (tabulation dans ce cas '\t')
df = pd.read_csv('ACCOR_2024-10-24.txt', sep='\t', parse_dates=['date'])

# Extraire la première colonne
premiere_colonne = df['bas']
x1 = np.array(premiere_colonne)

x1 = x1/np.sqrt(np.dot(x1,x1))


x2 = pd.read_csv('AIRLIQUIDE_2024-10-24.txt', sep='\t', parse_dates=['date'])

# Extraire la première colonne
premiere_colonne = x2['bas']
x2 = np.array(premiere_colonne)

x2 = x2/np.sqrt(np.dot(x2,x2))
plt.plot(x1,label='accor')
plt.plot(x2,label='airliquid')
plt.legend()
plt.show()


ndim=2
A=np.ones((ndim,ndim))

A[0,1] = np.sqrt(np.dot(x1,x2))
A[1,0] = A[0,1]

nt = len(x1)
r1=0
r2=0
for i in range(nt-1):
    r1+=(x1[i+1]-x1[i]/x1[i])
    r2+=(x2[i+1]-x2[i]/x2[i])

r1/=nt
r2/=nt

print("R Accord",r1,"R AL",r2)

R=0.5*(r1+r2)

# %%

