# Mini-projet – Ordonnancement CPU

> Note: This project is currently documented in French.

## Présentation
Ce projet simule l’ordonnancement des processus dans un système
d’exploitation. Il permet de comparer plusieurs algorithmes classiques
à l’aide de métriques concrètes comme le temps d’attente, le temps de
rotation et le débit.

Le programme fonctionne en mode console et repose sur une saisie
interactive des données.

## Algorithmes implémentés
- FCFS (First Come First Served)
- SJF non préemptif
- SRTF (Shortest Remaining Time First)
- Priorité non préemptive
- Priorité préemptive
- Round Robin

## Fonctionnalités
- Saisie des processus (durée, priorité, temps d’arrivée)
- Affichage du diagramme de Gantt
- Calcul du temps moyen d’attente
- Calcul du temps moyen de rotation
- Calcul du débit sur un intervalle donné
- Comparaison et classement des algorithmes

## Technologies utilisées
- Python
- Bibliothèques standard : `time`, `collections (deque)`

## Structure du projet 
```
mini-projet-ordonnancement/
├── src/
│ └── main.py
└── README.md
```


## Exécution
Depuis le dossier du projet :
```bash
python src/main.py
```

## Auteur
Redallah Tarkaoui
