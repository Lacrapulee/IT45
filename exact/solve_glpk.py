import pulp as pl
import sys
import time

def load_instance(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    n = 0
    m = 0
    p = {}
    
    reading_p = False
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('param n :='):
            n = int(line.split(':=')[1].replace(';', ''))
        elif line.startswith('param m :='):
            m = int(line.split(':=')[1].replace(';', ''))
        elif line.startswith('param p :='):
            reading_p = True
        elif reading_p:
            if line == ';':
                reading_p = False
            else:
                parts = line.split()
                if len(parts) == 2:
                    p[int(parts[0])] = int(parts[1])
    
    return n, m, [p[i] for i in range(1, n + 1)]

def solve_exact_glpk(n, m, p):
    # Création du problème de minimisation
    prob = pl.LpProblem("Ordonnancement_Bloc_GLPK", pl.LpMinimize)

    # Variables de décision
    # x[i][k] = 1 si le patient i est dans la salle k
    x = pl.LpVariable.dicts("x", (range(n), range(m)), cat=pl.LpBinary)
    Cmax = pl.LpVariable("Cmax", lowBound=0, cat=pl.LpContinuous)

    # Fonction objectif
    prob += Cmax

    # Contraintes
    # 1. Chaque patient est affecté à une seule salle
    for i in range(n):
        prob += pl.lpSum(x[i][k] for k in range(m)) == 1

    # 2. Le Makespan est supérieur ou égal au temps d'occupation de chaque salle
    for k in range(m):
        prob += pl.lpSum(p[i] * x[i][k] for i in range(n)) <= Cmax

    # Appel du solveur GLPK (msg=False désactive les logs verbeux dans le terminal)
    solver = pl.GLPK_CMD(msg=False)
    
    start_time = time.time()
    status = prob.solve(solver)
    end_time = time.time()

    if status == pl.LpStatusOptimal:
        return pl.value(prob.objective), end_time - start_time
    else:
        return None, None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python solve_glpk.py <instance_file>")
        sys.exit(1)
        
    instance_file = sys.argv[1]
    n, m, p = load_instance(instance_file)
    
    val, duration = solve_exact_glpk(n, m, p)
    if val is not None:
        # Garde exactement la même chaîne de caractères pour que ton benchmark la détecte
        print(f"Valeur optimale (Cmax): {val}")
        print(f"Temps de résolution: {duration:.4f} secondes")
    else:
        print("Pas de solution optimale trouvée.")