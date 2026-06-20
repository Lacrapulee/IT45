import gurobipy as gp
from gurobipy import GRB
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

def solve_exact(n, m, p):
    model = gp.Model("Ordonnancement_Bloc")
    #model.setParam('OutputFlag', 0) # Désactiver les logs Gurobi

    # Variables
    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")
    Cmax = model.addVar(vtype=GRB.CONTINUOUS, name="Cmax")

    # Objectif
    model.setObjective(Cmax, GRB.MINIMIZE)

    # Contraintes
    # Chaque patient affecté à une salle
    for i in range(n):
        model.addConstr(gp.quicksum(x[i, k] for k in range(m)) == 1)

    # Makespan
    for k in range(m):
        model.addConstr(gp.quicksum(p[i] * x[i, k] for i in range(n)) <= Cmax)

    start_time = time.time()
    model.optimize()
    end_time = time.time()

    if model.status == GRB.OPTIMAL:
        return model.objVal, end_time - start_time
    else:
        return None, None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python solve_gurobi.py <instance_file>")
        sys.exit(1)
        
    instance_file = sys.argv[1]
    n, m, p = load_instance(instance_file)
    
    val, duration = solve_exact(n, m, p)
    if val is not None:
        print(f"Valeur optimale (Cmax): {val}")
        print(f"Temps de résolution: {duration:.4f} secondes")
    else:
        print("Pas de solution optimale trouvée.")
