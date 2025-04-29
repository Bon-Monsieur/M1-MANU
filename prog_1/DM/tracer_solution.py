import os
import matplotlib.pyplot as plt

def lire_fichier(fichier):
    abscisses = []
    valeurs = []

<<<<<<< HEAD
    with open(fichier) as f:
        for ligne in f:
            if ligne.strip():  # Ignore les lignes vides
                x, u = map(float, ligne.split())
                abscisses.append(x)
                valeurs.append(u)
=======
    print("Chemin courant :", os.getcwd())
    print("Tentative d'ouverture de :", fichier)
>>>>>>> 9c2840731e867c3d24497a75da669a07941a4ece

    try:
        with open(fichier, 'r') as f:
            for ligne in f:
                if ligne.strip():
                    x, u = map(float, ligne.split())
                    abscisses.append(x)
                    valeurs.append(u)
    except FileNotFoundError:
        print(f"Fichier non trouvé : {fichier}")
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")

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
