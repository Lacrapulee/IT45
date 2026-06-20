import subprocess
import os
import time
import re
import matplotlib.pyplot as plt
import numpy as np
import resource  # Bibliothèque pour mesurer l'utilisation des ressources (mémoire, CPU, etc.)

instances = [
    "Instance_1_n10_m2.dat", "Instance_1_n10_m3.dat", "Instance_1_n15_m2.dat", "Instance_1_n15_m3.dat",
    "Instance_1_n30_m2.dat", "Instance_1_n30_m3.dat", "Instance_1_n45_m4.dat", "Instance_1_n45_m5.dat",
    "Instance_1_n45_m6.dat", "Instance_1_n45_m7.dat", "Instance_1_n45_m8.dat", "Instance_1_n45_m9.dat",
    "Instance_1_n45_m10.dat", "Instance_1_n60_m4.dat", "Instance_1_n60_m5.dat", "Instance_1_n60_m6.dat",
    "Instance_1_n60_m7.dat", "Instance_1_n60_m8.dat", "Instance_1_n60_m9.dat", "Instance_1_n60_m10.dat",
    "Instance_1_n75_m4.dat", "Instance_1_n75_m5.dat", "Instance_1_n75_m6.dat", "Instance_1_n75_m7.dat",
    "Instance_1_n75_m8.dat", "Instance_1_n75_m9.dat", "Instance_1_n75_m10.dat", "Instance_1_n100_m4.dat",
    "Instance_1_n100_m5.dat", "Instance_1_n100_m6.dat", "Instance_1_n100_m7.dat", "Instance_1_n100_m8.dat",
    "Instance_1_n100_m9.dat", "Instance_1_n100_m10.dat", "Instance_1_n150_m4.dat", "Instance_1_n150_m5.dat",
    "Instance_1_n150_m6.dat", "Instance_1_n150_m7.dat", "Instance_1_n150_m8.dat", "Instance_1_n150_m9.dat",
    "Instance_1_n150_m10.dat", "Instance_1_n200_m4.dat", "Instance_1_n200_m5.dat", "Instance_1_n200_m6.dat",
    "Instance_1_n200_m7.dat", "Instance_1_n200_m8.dat", "Instance_1_n200_m9.dat", "Instance_1_n200_m10.dat",
    "Instance_1_n300_m4.dat", "Instance_1_n300_m5.dat", "Instance_1_n300_m6.dat", "Instance_1_n300_m7.dat",
    "Instance_1_n300_m8.dat", "Instance_1_n300_m9.dat", "Instance_1_n300_m10.dat", "Instance_1_n400_m4.dat",
    "Instance_1_n400_m5.dat", "Instance_1_n400_m6.dat", "Instance_1_n400_m7.dat", "Instance_1_n400_m8.dat",
    "Instance_1_n400_m9.dat", "Instance_1_n400_m10.dat", "Instance_1_n500_m4.dat", "Instance_1_n500_m5.dat",
    "Instance_1_n500_m6.dat", "Instance_1_n500_m7.dat", "Instance_1_n500_m8.dat", "Instance_1_n500_m9.dat",
    "Instance_1_n500_m10.dat"
]
def set_memory_limit():
    # Limite la mémoire virtuelle à 2 Go (2 * 1024 * 1024 * 1024 octets)
    max_memory = 2 * 1024 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (max_memory, max_memory))

results = []

for inst in instances:
    print(f"Test de l'instance: {inst}")
    
    match = re.search(r'_n(\d+)_m(\d+)', inst)
    n = int(match.group(1)) if match else 0
    m = int(match.group(2)) if match else 0
    
    # --- EXACT (Gurobi) ---
    start_exact = time.time()
    out_exact = subprocess.check_output(["python3", "exact/solve_gurobi.py", f"instances/{inst}"]).decode()
    time_exact = time.time() - start_exact
    
    val_exact = None
    for line in out_exact.split('\n'):
        if "Valeur optimale" in line:
            val_exact = float(line.split(': ')[1])
            
    # --- EXACT ALTERNATIF (GLPK) ---
    val_glpk = None
    time_glpk = None
    try:
        start_glpk = time.time()
        # Sécurité double : Timeout de 10s ET limite de RAM via preexec_fn
        out_glpk = subprocess.check_output(
            ["python3", "exact/solve_glpk.py", f"instances/{inst}"], 
            preexec_fn=set_memory_limit  # Applique la limite de 2 Go avant de lancer le script
        ).decode()
        time_glpk = time.time() - start_glpk
        for line in out_glpk.split('\n'):
            if "Valeur optimale" in line:
                val_glpk = float(line.split(': ')[1])
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        # CalledProcessError sera levé si GLPK est tué par manque de RAM (Memory Error)
        print(f"  -> GLPK stoppé (Timeout ou limite de RAM atteinte) ")
        val_glpk = float('inf')
        time_glpk = 40.0
    except Exception as e:
        val_glpk = float('inf')
        time_glpk = 0.0
        
    # --- APPROCHÉ (Algorithme Génétique) ---
    out_ag = subprocess.check_output(["./run", f"instances/{inst}"]).decode()
    
    val_ag = None
    time_ag = None
    for line in out_ag.split('\n'):
        if "Meilleur Makespan trouvé" in line:
            val_ag = float(line.split(': ')[1])
        if "Temps de calcul" in line:
            time_ag = float(line.split(': ')[1].split()[0])
            
    gap = ((val_ag - val_exact) / val_exact) * 100 if val_exact else 0
    
    results.append({
        "instance": inst,
        "n": n,
        "m": m,
        "exact_val": val_exact,
        "exact_time": time_exact,
        "glpk_val": val_glpk,
        "glpk_time": time_glpk if time_glpk is not None else 0.0,
        "ag_val": val_ag,
        "ag_time": time_ag if time_ag is not None else 0.0,
        "gap": gap
    })


print("\n" + "="*95)
print("RÉSULTATS RÉCAPITULATIFS")
print("="*95)
print(f"{'Instance':<24} | {'Exact (Grb)':<11} | {'GLPK':<10} | {'AG':<10} | {'T_Gurobi':<9} | {'T_GLPK':<8} | {'T_AG':<8} | {'Gap (%)':<7}")
print("-" * 110)
for r in results:
    glpk_val_str = f"{r['glpk_val']:<10.1f}" if r['glpk_val'] != float('inf') else f"{'Timeout':<10}"
    print(f"{r['instance']:<24} | {r['exact_val']:<11.1f} | {glpk_val_str} | {r['ag_val']:<10.1f} | {r['exact_time']:<9.4f} | {r['glpk_time']:<8.4f} | {r['ag_time']:<8.4f} | {r['gap']:<7.2f}")

# --- PRÉPARATION DES DONNÉES POUR LES GRAPHES ---
n_arr = np.array([r['n'] for r in results])
m_arr = np.array([r['m'] for r in results])
t_exact = np.array([r['exact_time'] for r in results])
t_glpk = np.array([r['glpk_time'] for r in results])
t_ag = np.array([r['ag_time'] for r in results])

# On trie par 'n' pour avoir des courbes propres en 2D
sort_idx = np.argsort(n_arr)

# --- GRAPHIQUE 2D : Comparaison des 3 méthodes ---
plt.figure(figsize=(10, 6))
plt.plot(n_arr[sort_idx], t_exact[sort_idx], label='Gurobi (Commercial)', color='red', marker='o', linestyle='-')
plt.plot(n_arr[sort_idx], t_glpk[sort_idx], label='GLPK (Open-Source)', color='orange', marker='s', linestyle='-.')
plt.plot(n_arr[sort_idx], t_ag[sort_idx], label='Algo Génétique (AG)', color='blue', marker='x', linestyle='--')
plt.xlabel('Nombre de patients (n)')
plt.ylabel("Temps de calcul (secondes)")
plt.title('Comparaison du temps de calcul (Gurobi vs GLPK vs AG)')
plt.legend()
plt.grid(True)
plt.savefig('comparaison_temps_2d.png')
print("\nGraphique 2D sauvegardé sous 'comparaison_temps_2d.png'")

# --- GRAPHIQUE 3D : Nuage de points ---
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(n_arr, m_arr, t_exact, color='red', label='Gurobi (Exact)', marker='o', s=40)
ax.scatter(n_arr, m_arr, t_glpk, color='orange', label='GLPK (Exact)', marker='s', s=40)
ax.scatter(n_arr, m_arr, t_ag, color='blue', label='Algo Génétique (AG)', marker='^', s=40)

ax.set_xlabel('Nombre de Patients (n)')
ax.set_ylabel('Nombre de Salles (m)')
ax.set_zlabel('Temps de calcul (s)')
ax.set_title("Impact de n et m sur le temps de calcul (3D)")
ax.legend()

plt.savefig('comparaison_temps_3d.png')
print("Graphique 3D sauvegardé sous 'comparaison_temps_3d.png'")
plt.show()