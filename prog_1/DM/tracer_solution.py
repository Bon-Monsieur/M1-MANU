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

    plt.plot(abscisses, valeurs, marker='.', linestyle='-')
    plt.xlabel("Abscisse (x)")
    plt.ylabel("Valeur (u)")
    plt.title("Profil de la solution")
    plt.grid(True)
    plt.show()

# Exemple d’utilisation :
# Remplace "resultats_0.txt" par le nom exact de ton fichier
lire_et_tracer("solution_0.txt")