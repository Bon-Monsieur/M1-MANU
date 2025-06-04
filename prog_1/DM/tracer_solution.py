import os
import matplotlib.pyplot as plt

def lire_fichier(fichier):
    abscisses = []
    valeurs = []

    with open(fichier,'r') as f:
        for ligne in f:
            if ligne.strip():  # Ignore les lignes vides
                x, u = map(float, ligne.split())
                abscisses.append(x)
                valeurs.append(u)

    return abscisses, valeurs


# Lecture des deux fichiers
x_init, u_init = lire_fichier("GAUSS_PULSE_initial.txt")
x_final, u_final = lire_fichier("GAUSS_PULSE_final.txt")

# Tracé sur le même graphique
plt.plot(x_init, u_init, label="Solution initiale", linestyle='--', color='blue')
plt.plot(x_final, u_final, label="Solution finale", linestyle='-', color='red')

plt.xlabel("Abscisse (x)")
plt.ylabel("Valeur (u)")
plt.title("Comparaison solution initiale et finale")
plt.grid(True)
plt.legend()
plt.show()
