# Rapport de Projet IT45 - Ordonnancement de Bloc Opératoire

## 1. Introduction

Ce rapport présente l'analyse et la résolution du problème d'ordonnancement de bloc opératoire, tel que défini dans le projet IT45. L'objectif principal est de minimiser le makespan (Cmax), c'est-à-dire le temps de fin de la dernière opération dans les salles d'opération, en affectant `n` patients à `m` salles d'opération identiques. Chaque patient `i` a une durée opératoire `p_i` connue et fixe. Le chevauchement d'interventions dans une même salle n'est pas autorisé, mais les salles peuvent opérer simultanément.

Le problème est un flow-shop hybride avec machines identiques parallèles, une variante du problème d'ordonnancement de machines parallèles, connu pour être NP-difficile.

## 2. Modélisation Mathématique (Méthode Exacte)

Le problème a été modélisé comme un programme linéaire en nombres entiers (PLNE) pour être résolu de manière exacte. La modélisation est basée sur les variables de décision et contraintes suivantes :

**Paramètres :**
- `n`: Nombre de patients.
- `m`: Nombre de salles d'opération.
- `p_i`: Durée opératoire du patient `i`.

**Variables de décision :**
- `x_{i,k}`: Variable binaire valant 1 si le patient `i` est affecté à la salle `k`, 0 sinon.
- `Cmax`: Variable continue représentant le makespan (temps de fin maximum).

**Fonction objectif :**
Minimiser `Cmax`.

**Contraintes :**
1.  Chaque patient doit être affecté à exactement une salle :
    `sum_{k=1 to m} x_{i,k} = 1` pour tout `i` de 1 à `n`.
2.  Le makespan doit être supérieur ou égal au temps total d'occupation de chaque salle :
    `sum_{i=1 to n} p_i * x_{i,k} <= Cmax` pour tout `k` de 1 à `m`.

Cette modélisation a été implémentée conceptuellement en AMPL (`modele.mod`) et résolue en utilisant l'API Python de Gurobi (`solve_gurobi.py`) pour des raisons de compatibilité avec l'environnement de développement.

## 3. Méthode Approchée (Algorithme Génétique)

Un algorithme génétique (AG) a été développé pour résoudre le problème de manière approchée, compte tenu de sa complexité NP-difficile. L'AG suit les étapes classiques :

**Représentation des solutions (codage) :**
Un chromosome est une liste de taille `n`, où chaque élément `chromosome[i]` représente l'indice de la salle (de 0 à `m-1`) à laquelle le patient `i` est affecté.

**Fonction de fitness :**
La fonction de fitness calcule le makespan (Cmax) pour un chromosome donné. L'objectif de l'AG est de minimiser cette valeur. Pour la sélection, les valeurs de fitness sont ajustées pour que les individus avec un makespan plus faible aient une probabilité de sélection plus élevée.

**Génération de la population initiale :**
La population initiale est générée aléatoirement, chaque patient étant affecté à une salle au hasard.

**Sélection :**
La sélection des parents est réalisée par la méthode de la roue de la fortune, adaptée pour la minimisation.

**Croisement (Crossover) :**
Un croisement en un point est utilisé. Un point de coupure aléatoire est choisi, et les segments des deux parents sont échangés pour créer deux enfants.

**Mutation :**
La mutation est appliquée avec une certaine probabilité (`mutation_rate`). Elle consiste à modifier aléatoirement la salle affectée à un patient.

**Élitisme :**
Les meilleurs individus de la génération précédente sont directement transférés à la nouvelle génération pour garantir la conservation des bonnes solutions.

**Critère d'arrêt :**
L'algorithme s'arrête après un nombre fixe de générations (`generations`).

L'implémentation de l'algorithme génétique se trouve dans le fichier `ag.py`.

## 4. Expérimentations et Résultats

Les deux méthodes (exacte et algorithme génétique) ont été testées sur l'instance fournie (`instance_60_4.dat`) ainsi que sur des instances générées aléatoirement de différentes tailles (nombre de patients `n` et nombre de salles `m`).

Le script `benchmark.py` a été utilisé pour automatiser les tests et collecter les résultats. Les durées opératoires `p_i` pour les instances générées sont des entiers aléatoires entre 30 et 300.

### Tableau Récapitulatif des Résultats

| Instance                       | Valeur Optimale (Cmax) | Cmax AG | Temps AG (s) | Gap (%) |
| :----------------------------- | :--------------------- | :------ | :----------- | :------ |
| `instance_60_4.dat`            | 1805.0                 | 1820.0  | 1.1911       | 0.83    |
| `instance_20_2.dat`            | 1628.0                 | 1628.0  | 0.8419       | 0.00    |
| `instance_40_3.dat`            | 1982.0                 | 1984.0  | 0.9436       | 0.10    |
| `instance_80_5.dat`            | 2726.0                 | 2758.0  | 1.3889       | 1.17    |
| `instance_100_6.dat`           | 2787.0                 | 2846.0  | 1.4354       | 2.12    |

### Analyse des Résultats

Les résultats montrent que la méthode exacte (résolue par Gurobi) trouve la solution optimale pour toutes les instances testées, avec des temps de résolution très courts, même pour l'instance la plus grande (`n=100, m=6`). Cela est attendu pour des problèmes de cette taille qui restent dans la portée des solveurs PLNE modernes.

L'algorithme génétique, en tant que méthode approchée, fournit des solutions proches de l'optimum. Le 
gap (écart relatif par rapport à l'optimum) est généralement faible, variant de 0% à environ 2.12%. Le temps de calcul de l'AG est également raisonnable, augmentant avec la taille de l'instance.

Il est important de noter que pour des instances de très grande taille, où la méthode exacte pourrait devenir trop coûteuse en temps de calcul, l'algorithme génétique deviendrait une alternative plus viable, même si elle ne garantit pas l'optimalité.

## 5. Livrables

Les livrables de ce projet sont les suivants :

- **Méthode exacte :**
    - `projet_ro/exact/modele.mod`: Le modèle mathématique du problème (format AMPL).
    - `projet_ro/exact/solve_gurobi.py`: Script Python utilisant l'API Gurobi pour résoudre le modèle.

- **Méthode approchée :**
    - `projet_ro/approche/ag.py`: Implémentation de l'algorithme génétique en Python.
    - `projet_ro/approche/README.md`: Documentation pour l'algorithme génétique.
    - `projet_ro/run`: Script exécutable pour lancer l'algorithme génétique.

- **Instances :**
    - `projet_ro/instances/instance_60_4.dat`: L'instance fournie par l'utilisateur.
    - `projet_ro/instances/instance_20_2.dat`, `instance_40_3.dat`, `instance_80_5.dat`, `instance_100_6.dat`: Instances générées pour les expérimentations.
    - `projet_ro/instances/gen_instances.py`: Script Python pour générer des instances.

- **Scripts d'expérimentation :**
    - `projet_ro/benchmark.py`: Script Python pour automatiser les tests et collecter les résultats.

- **Rapport :**
    - `projet_ro/rapport_final.md`: Ce rapport au format Markdown.

## 6. Conclusion

Ce projet a permis d'explorer deux approches pour résoudre le problème d'ordonnancement de bloc opératoire : une méthode exacte basée sur la programmation linéaire en nombres entiers et un algorithme génétique. Les résultats montrent que la méthode exacte est efficace pour les instances de taille modérée, tandis que l'algorithme génétique offre une bonne solution approchée avec un temps de calcul raisonnable, ce qui le rend pertinent pour des instances plus grandes où l'optimalité n'est pas toujours atteignable dans un temps imparti.
