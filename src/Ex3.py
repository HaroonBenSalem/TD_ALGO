import math
import random

random.seed(1)
PENALITE = 1000

routes = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}
NB_VILLES = 8


def distance(a, b):
    if (a, b) in routes:
        return routes[(a, b)]
    if (b, a) in routes:
        return routes[(b, a)]
    return PENALITE


def cout(tour):
    total = 0
    for k in range(len(tour)):
        total += distance(tour[k], tour[(k + 1) % len(tour)])
    return total


def afficher(tour):
    return "-".join(str(v) for v in tour) + "-1"


def deplacer(tour, i, j):
    """Voisin par insertion : on retire la ville à la position i
    et on la remet à la position j."""
    nouveau = tour[:]
    ville = nouveau.pop(i)
    nouveau.insert(j, ville)
    return nouveau


# 1) Recherche taboue
def recherche_taboue(nb_iterations=10, taille_tabou=3):
    courant = [1, 2, 3, 4, 5, 6, 7, 8]
    meilleur = courant[:]
    cout_meilleur = cout(courant)
    tabou = []

    print("=== Recherche taboue ===")
    print("Solution initiale :", afficher(courant), "| coût =", cout_meilleur)
    print("Iter | Ville déplacée | Nouveau tour      | Coût | Meilleur")

    for it in range(1, nb_iterations + 1):
        choix = None
        for i in range(1, NB_VILLES):
            for j in range(1, NB_VILLES):
                if i == j:
                    continue
                voisin = deplacer(courant, i, j)
                c = cout(voisin)
                mvt = courant[i]
                if mvt in tabou and c >= cout_meilleur:
                    continue
                if choix is None or c < choix[2]:
                    choix = (mvt, voisin, c)

        mvt, courant, c = choix
        tabou.append(mvt)
        if len(tabou) > taille_tabou:
            tabou.pop(0)

        if c < cout_meilleur:
            cout_meilleur = c
            meilleur = courant[:]

        print(f"{it:4d} | {mvt:14d} | {afficher(courant)} | {c:4d} | {cout_meilleur:4d}")

    print("Meilleur tour :", afficher(meilleur), "| coût =", cout_meilleur)
    print()
    return meilleur, cout_meilleur



# 2) Recuit simulé (5 itérations)
def recuit_simule():
    courant = [1, 2, 3, 4, 5, 6, 7, 8]
    meilleur = courant[:]
    temperatures = [30, 20, 12, 6, 2]

    print("=== Recuit simulé ===")
    print("Solution initiale :", afficher(courant), "| coût =", cout(courant))
    print("Iter |  T | Voisin            | Coût | Delta | Décision")

    for it, T in enumerate(temperatures, start=1):
        i, j = random.sample(range(1, NB_VILLES), 2)
        voisin = deplacer(courant, i, j)
        delta = cout(voisin) - cout(courant)

        if delta < 0:
            accepte = True
            decision = "accepté (meilleur)"
        else:
            p = math.exp(-delta / T)
            r = random.random()
            accepte = r < p
            decision = f"p={p:.3f}, r={r:.3f} -> " + ("accepté" if accepte else "refusé")

        if accepte:
            courant = voisin
            if cout(courant) < cout(meilleur):
                meilleur = courant[:]

        print(f"{it:4d} | {T:2d} | {afficher(voisin)} | {cout(voisin):4d} | {delta:5d} | {decision}")

    print("Meilleur tour :", afficher(meilleur), "| coût =", cout(meilleur))
    print()
    return meilleur, cout(meilleur)



# 3) Algorithme génétique
def croisement(parent1, parent2):
    a, b = sorted(random.sample(range(len(parent1)), 2))
    enfant = [None] * len(parent1)
    enfant[a:b] = parent1[a:b]
    restant = [v for v in parent2 if v not in enfant]
    k = 0
    for pos in range(len(enfant)):
        if enfant[pos] is None:
            enfant[pos] = restant[k]
            k += 1
    return enfant


def mutation(individu, proba=0.2):
    if random.random() < proba:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu


def selection(population):
    a, b = random.sample(population, 2)
    return a if cout([1] + a) < cout([1] + b) else b


def algorithme_genetique(taille_pop=10, nb_generations=15):
    villes = list(range(2, NB_VILLES + 1))
    population = []
    for _ in range(taille_pop):
        ind = villes[:]
        random.shuffle(ind)
        population.append(ind)

    print("=== Algorithme génétique ===")
    print(f"Population = {taille_pop}, générations = {nb_generations}, mutation = 0.2")
    print("Gén | Meilleur tour     | Coût")

    meilleur = None
    for g in range(1, nb_generations + 1):
        population.sort(key=lambda ind: cout([1] + ind))

        if meilleur is None or cout([1] + population[0]) < cout([1] + meilleur):
            meilleur = population[0][:]

        print(f"{g:3d} | {afficher([1] + population[0])} | {cout([1] + population[0]):4d}")

        nouvelle = [population[0][:], population[1][:]]
        while len(nouvelle) < taille_pop:
            p1 = selection(population)
            p2 = selection(population)
            enfant = croisement(p1, p2)
            enfant = mutation(enfant)
            nouvelle.append(enfant)
        population = nouvelle

    tour = [1] + meilleur
    print("Meilleur tour :", afficher(tour), "| coût =", cout(tour))
    print()
    return tour, cout(tour)


if __name__ == "__main__":
    recherche_taboue()
    recuit_simule()
    algorithme_genetique()