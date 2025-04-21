import os
import matplotlib.pyplot as plt

def lire_et_tracer(fichier):
    abscisses = []
    valeurs = []

    print("Chemin courant :", os.getcwd())
    print("Tentative d'ouverture de :", fichier)

    try:
        with open(fichier, 'r') as f:
            for ligne in f:
                if ligne.strip():
                    x, u = map(float, ligne.split())
                    abscisses.append(x)
                    valeurs.append(u)

        plt.plot(abscisses, valeurs)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Solution approchée")
        plt.xlim(0, 10)
        plt.ylim(-0.2, 1.2)
        plt.grid(True)
        plt.show()
    except FileNotFoundError:
        print(f"Fichier non trouvé : {fichier}")
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")

lire_et_tracer("GAUSS_PULSE_final.txt")
