# Problème d'ordonnancement de bloc opératoire
# Minimisation du Makespan (Cmax) sur m machines identiques

param n; # Nombre de patients
param m; # Nombre de salles d'opération

set I := 1..n; # Ensemble des patients
set K := 1..m; # Ensemble des salles

param p{I}; # Durée opératoire de chaque patient i

# Variables de décision
var x{I, K} binary; # x[i,k] = 1 si le patient i est affecté à la salle k, 0 sinon
var Cmax >= 0;      # Makespan

# Fonction objectif
minimize Total_Time: Cmax;

# Contraintes
# 1. Chaque patient doit être affecté à exactement une salle
subject to Affectation {i in I}:
    sum {k in K} x[i,k] = 1;

# 2. Le Makespan est supérieur ou égal au temps total d'occupation de chaque salle
subject to Makespan_Constraint {k in K}:
    sum {i in I} p[i] * x[i,k] <= Cmax;
