# Algorithme Génétique pour l'Ordonnancement de Bloc Opératoire

Ce répertoire contient l'implémentation d'un algorithme génétique (AG) pour résoudre le problème d'ordonnancement de bloc opératoire, visant à minimiser le makespan (Cmax) sur `m` machines parallèles identiques.

## Fichiers

- `ag.py`: Le script Python implémentant l'algorithme génétique.
- `README.md`: Ce fichier.

## Utilisation

Pour exécuter l'algorithme génétique sur une instance donnée, utilisez le script `run` à la racine du projet :

```bash
./run instances/nom_de_l_instance.dat
```

Par exemple, pour l'instance `instance_60_4.dat` :

```bash
./run instances/instance_60_4.dat
```

Le script affichera le meilleur makespan trouvé et le temps de calcul.

## Paramètres de l'AG

Les paramètres de l'algorithme génétique peuvent être ajustés dans la classe `GeneticAlgorithm` du fichier `ag.py` :

- `pop_size`: Taille de la population (par défaut : 100)
- `generations`: Nombre de générations (par défaut : 500)
- `crossover_rate`: Taux de croisement (par défaut : 0.8)
- `mutation_rate`: Taux de mutation (par défaut : 0.1)
- `elitism_count`: Nombre d'individus élitistes conservés (par défaut : 2)

## Structure du Chromosome

Un chromosome est représenté par une liste de taille `n` (nombre de patients), où `chromosome[i]` indique la salle (`0` à `m-1`) à laquelle le patient `i` est affecté.

## Fonction de Fitness

La fonction de fitness calcule le makespan (Cmax) d'un chromosome donné. L'objectif est de minimiser cette valeur.

## Sélection

La sélection est effectuée par la méthode de la roue de la fortune, adaptée pour la minimisation.

## Croisement (Crossover)

Un croisement en un point est utilisé, où un point de coupure aléatoire est choisi, et les segments des parents sont échangés pour créer deux enfants.

## Mutation

La mutation consiste à changer aléatoirement la salle affectée à un patient avec une certaine probabilité (`mutation_rate`).
