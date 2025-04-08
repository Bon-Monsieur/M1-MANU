import matplotlib.pyplot as plt

def lire_et_tracer(fichier):
    abscisses = []
    valeurs = []

    with open(fichier, 'r') as f:
        for ligne in f:
            if ligne.strip():  # Ignore les lignes vides
                x, u = map(float, ligne.split())
                abscisses.append(x)
                valeurs.append(u)

    plt.plot(abscisses, valeurs)
    plt.xlabel("Abscisse (x)")
    plt.ylabel("Valeur (u)")
    plt.title("Tracé des valeurs")
    plt.grid(True)
    plt.show()

lire_et_tracer("GAUSS_PULSE_initial.txt")