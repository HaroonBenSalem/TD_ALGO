couts = [[5, 3, 4],
         [6, 7, 2]]
stock = [8, 9]
demande = [4, 5, 8]

depots = len(stock)
magasins = len(demande)


def cout_total(x):
    total = 0
    for i in range(depots):
        for j in range(magasins):
            total += couts[i][j] * x[i][j]
    return total

def solution_initiale():
    x = [[0] * magasins for _ in range(depots)]
    s = stock[:]
    d = demande[:]
    i, j = 0, 0
    while i < depots and j < magasins:
        q = min(s[i], d[j])
        x[i][j] = q
        s[i] -= q
        d[j] -= q
        if s[i] == 0:
            i += 1
        else:
            j += 1
    return x

def voisins(x):
    liste = []
    for i1 in range(depots):
        for i2 in range(i1 + 1, depots):
            for j1 in range(magasins):
                for j2 in range(magasins):
                    if j1 == j2:
                        continue
                    if x[i1][j2] >= 1 and x[i2][j1] >= 1:
                        y = [ligne[:] for ligne in x]
                        y[i1][j1] += 1
                        y[i2][j2] += 1
                        y[i1][j2] -= 1
                        y[i2][j1] -= 1
                        liste.append(((i1, i2, j1, j2), y))
    return liste

def recherche_taboue(nb_iterations=10, taille_tabou=3):
    x = solution_initiale()
    meilleur = [ligne[:] for ligne in x]
    cout_meilleur = cout_total(x)
    tabou = []

    print("Solution initiale :", x, "| coût =", cout_meilleur)
    print()
    print("Iter | Mouvement      | Coût courant | Meilleur coût")

    for it in range(1, nb_iterations + 1):
        choix = None
        for mvt, y in voisins(x):
            c = cout_total(y)
            if mvt in tabou and c >= cout_meilleur:
                continue
            if choix is None or c < choix[2]:
                choix = (mvt, y, c)

        if choix is None:
            print("Plus de voisin autorisé, arrêt.")
            break

        mvt, x, c = choix

        i1, i2, j1, j2 = mvt
        tabou.append((i1, i2, j2, j1))
        if len(tabou) > taille_tabou:
            tabou.pop(0)

        if c < cout_meilleur:
            cout_meilleur = c
            meilleur = [ligne[:] for ligne in x]

        print(f"{it:4d} | {str(mvt):14s} | {c:12d} | {cout_meilleur:13d}")

    return meilleur, cout_meilleur

if __name__ == "__main__":
    sol, cout = recherche_taboue()
    print()
    print("Meilleure solution trouvée :")
    for i in range(depots):
        print(f"  D{i + 1} ->", sol[i])
    print("Coût total minimal =", cout)

