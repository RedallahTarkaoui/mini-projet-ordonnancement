import time # Importe le module time pour gérer le temps (horloge système)
from collections import deque # Importe deque (file) depuis collections pour l’algorithme Round Robin

# FONCTIONS COMMUNES  :
def afficher_gantt(gantt): # Liste dont chaque element est un tuple !
    print("Gantt :", end=" ")
    for pid, d, f in gantt:
        print(f"| {pid} [{d}-{f}] ", end="")
    print("|")

def afficher_processus(processus):
    print("\n--- Liste des processus ---")
    print(f"{'ID':<5}{'Durée':<8}{'Priorité':<10}{'Arrivée':<8}")
    for p in processus:
        print(f"{p['id']:<5}{p['duree']:<8}{p['priorite']:<10}{p['arrivee']:<8}")
    print("-" * 40)

def calcul_throughput_interval(gantt, intervalle):
    """
    Débit = nombre de processus terminés avant ou à l’instant intervalle
            divisé par la durée de l’intervalle
    """
    fins = {} # Dictionnaire pour stocker la fin de chaque processus
    # On récupère la vraie fin de chaque processus
    for pid, d, f in gantt:
        fins[pid] = f

    # On compte combien de processus sont terminés avant l'intervalle
    termines = sum(1 for f in fins.values() if f <= intervalle)

    return termines / intervalle if intervalle > 0 else 0

# FCFS :

def fcfs(processus):
    # On trie les processus selon leur temps d'arrivée
    processus = sorted(processus, key=lambda x: x['arrivee'])

    temps = 0
    gantt = []
    attente = rotation = 0

    for p in processus:
        # Si le CPU est libre, on avance le temps
        if temps < p['arrivee']:
            temps = p['arrivee']

        debut = temps # Le processus commence à l’instant actuel du CPU
        temps += p['duree']
        fin = temps

        # Calculs des temps
        attente += debut - p['arrivee']
        rotation += fin - p['arrivee']

        gantt.append((p['id'], debut, fin))

    return gantt, attente / len(processus), rotation / len(processus)

# SJF NON PRÉEMPTIF :

def sjf_np(processus):
    fini = [False] * len(processus) # liste des processus terminés  
    temps = 0
    gantt = []
    attente = rotation = 0

    while not all(fini):
        # Processus disponibles à l'instant temps
        dispo = [(i, p) for i, p in enumerate(processus)
                 if not fini[i] and p['arrivee'] <= temps]

        # Aucun processus prêt → on avance le temps
        if not dispo:
            temps += 1
            continue

        # Choisir le processus avec la durée la plus courte
        i, p = min(dispo, key=lambda x: x[1]['duree'])

        debut = temps
        temps += p['duree']
        fin = temps

        attente += debut - p['arrivee']
        rotation += fin - p['arrivee']

        fini[i] = True
        gantt.append((p['id'], debut, fin))

    return gantt, attente / len(processus), rotation / len(processus)

# SRTF :

def srtf(processus):
    reste = [p['duree'] for p in processus]  # stocke le temps d’exécution restant de chaque processus
    fini = [False] * len(processus)  # liste des processus terminés

    temps = 0
    gantt = []
    attente = rotation = 0

    courant = None       # processus en cours
    debut_bloc = 0       # début du bloc courant dans le Gantt

    while not all(fini):
        # Processus disponibles
        dispo = [(i, p) for i, p in enumerate(processus)
                 if not fini[i] and p['arrivee'] <= temps]

        if not dispo:
            temps += 1
            continue

        # Choisir le processus avec le temps restant minimal
        i, p = min(dispo, key=lambda x: reste[x[0]])

        # Changement de processus → nouveau bloc Gantt 
        if courant != p['id']:
            if courant is not None:
                gantt.append((courant, debut_bloc, temps))
            courant = p['id']
            debut_bloc = temps

        # Exécution pendant 1 unité de temps
        reste[i] -= 1
        temps += 1

        # Si le processus se termine
        if reste[i] == 0:
            fini[i] = True
            fin = temps

            attente += fin - p['duree'] - p['arrivee']
            rotation += fin - p['arrivee']

            gantt.append((p['id'], debut_bloc, fin))
            courant = None

    return gantt, attente / len(processus), rotation / len(processus)

# PRIORITÉ NON PRÉEMPTIVE :

def priorite_np(processus):
    fini = [False] * len(processus)
    temps = 0
    gantt = []
    attente = rotation = 0

    while not all(fini):
        dispo = [(i, p) for i, p in enumerate(processus)
                 if not fini[i] and p['arrivee'] <= temps]

        if not dispo:
            temps += 1
            continue

        # Choisir le processus avec la meilleure priorité
        i, p = min(dispo, key=lambda x: x[1]['priorite'])

        debut = temps
        temps += p['duree']
        fin = temps

        attente += debut - p['arrivee']
        rotation += fin - p['arrivee']

        fini[i] = True
        gantt.append((p['id'], debut, fin))

    return gantt, attente / len(processus), rotation / len(processus)

# PRIORITÉ PRÉEMPTIVE :

def priorite_p(processus):
    reste = [p['duree'] for p in processus]
    fini = [False] * len(processus)

    temps = 0
    gantt = []
    attente = rotation = 0

    courant = None
    debut_bloc = 0

    while not all(fini):
        dispo = [(i, p) for i, p in enumerate(processus)
                 if not fini[i] and p['arrivee'] <= temps]

        if not dispo:
            temps += 1
            continue

        # Choix par priorité
        i, p = min(dispo, key=lambda x: x[1]['priorite'])

        if courant != p['id']:
            if courant is not None:
                gantt.append((courant, debut_bloc, temps))
            courant = p['id']
            debut_bloc = temps

        reste[i] -= 1
        temps += 1

        if reste[i] == 0:
            fini[i] = True
            fin = temps

            attente += fin - p['duree'] - p['arrivee']
            rotation += fin - p['arrivee']

            gantt.append((p['id'], debut_bloc, fin))
            courant = None

    return gantt, attente / len(processus), rotation / len(processus)

# ROUND ROBIN :

def round_robin(processus, quantum):
    reste = [p['duree'] for p in processus]
    fini = [False] * len(processus)

    file = deque()  # file circulaire
    temps = 0
    gantt = []
    attente = rotation = 0

    # Ajouter les processus arrivés à t = 0
    for i, p in enumerate(processus):
        if p['arrivee'] == 0:
            file.append(i)
    while not all(fini):
        if not file:
            temps += 1
            for i, p in enumerate(processus):
                if p['arrivee'] <= temps and not fini[i] and i not in file:
                    file.append(i)
            continue
# retire le premier indice de la file d’attente et récupère le processus correspondant pour l’exécuter.
        i = file.popleft()
        p = processus[i]

        debut = temps
        exec_t = min(quantum, reste[i])
        temps += exec_t
        reste[i] -= exec_t

        gantt.append((p['id'], debut, temps))

        # Ajouter les nouveaux processus arrivés
        for j, px in enumerate(processus):
            if px['arrivee'] <= temps and not fini[j] and j not in file:
                file.append(j)

        # Si le processus n'est pas fini, il retourne en file
        if reste[i] > 0:
            file.append(i)
        else:
            fini[i] = True
            attente += temps - p['duree'] - p['arrivee']
            rotation += temps - p['arrivee']

    return gantt, attente / len(processus), rotation / len(processus)

# PROGRAMME PRINCIPAL :

def main():
    print("=== Mini-Projet Ordonnancement CPU ===")

    n = int(input("Nombre de processus : "))
    processus = []

    for i in range(n):
        print(f"\nProcessus PR{i}")
        duree = int(input("Durée d'exécution : "))
        priorite = int(input("Priorité : "))

        # Le premier processus arrive à 0
        if i == 0:
            arrivee = 0
            temps_ref = time.time()
        else:
            arrivee = int(time.time() - temps_ref) # C’est l’instant exact où le premier processus est saisi. Il sert de point de départ pour calculer le temps d’arrivée des autres processus, en mesurant le temps écoulé depuis ce moment.

        processus.append({
            "id": f"PR{i}",
            "duree": duree,
            "priorite": priorite,
            "arrivee": arrivee
        })

    afficher_processus(processus)

    quantum = int(input("\nQuantum Round Robin : "))
    intervalle = int(input("Intervalle de temps pour le débit : "))

    algos = {
        "FCFS": fcfs,
        "SJF_NP": sjf_np,
        "SRTF": srtf,
        "PRIORITE_NP": priorite_np,
        "PRIORITE_P": priorite_p,
        "ROUND_ROBIN": lambda p: round_robin(p, quantum)
    }

    resultats = []

    for nom, algo in algos.items():
        gantt, att, rot = algo(processus)
        th = calcul_throughput_interval(gantt, intervalle)

        print(f"\n[{nom}]")
        afficher_gantt(gantt)
        print(f"Temps moyen d'attente   : {att:.2f}")
        print(f"Temps moyen de rotation : {rot:.2f}")
        print(f"Débit                   : {th:.2f}")

        resultats.append((nom, att, rot, th))

    # Classements finaux
    print("\n=== CLASSEMENTS ===")

    print("\n→ Par temps moyen d'attente :")
    for r in sorted(resultats, key=lambda x: x[1]):
        print(r[0])

    print("\n→ Par temps moyen de rotation :")
    for r in sorted(resultats, key=lambda x: x[2]):
        print(r[0])

    print("\n→ Par débit :")
    for r in sorted(resultats, key=lambda x: x[3], reverse=True):
        print(r[0])



if __name__ == "__main__":
      main()
