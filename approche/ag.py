import random
import time
import sys

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

class GeneticAlgorithm:
    def __init__(self, n, m, p, pop_size=100, generations=500, crossover_rate=0.8, mutation_rate=0.1, elitism_count=2):
        self.n = n
        self.m = m
        self.p = p
        self.pop_size = pop_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count

    def calculate_fitness(self, chromosome):
        # chromosome[i] = k (salle affectée au patient i)
        loads = [0] * self.m
        for i in range(self.n):
            loads[chromosome[i]] += self.p[i]
        return max(loads)

    def generate_initial_population(self):
        population = []
        for _ in range(self.pop_size):
            chromosome = [random.randint(0, self.m - 1) for _ in range(self.n)]
            population.append(chromosome)
        return population

    def selection_roulette(self, population, fitnesses):
        # On veut minimiser le fitness, donc on transforme
        max_fit = max(fitnesses)
        adjusted_fitnesses = [max_fit - f + 1 for f in fitnesses]
        total_fit = sum(adjusted_fitnesses)
        pick = random.uniform(0, total_fit)
        current = 0
        for i, f in enumerate(adjusted_fitnesses):
            current += f
            if current > pick:
                return population[i]
        return population[-1]

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, self.n - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1[:], parent2[:]

    def mutate(self, chromosome):
        for i in range(self.n):
            if random.random() < self.mutation_rate:
                chromosome[i] = random.randint(0, self.m - 1)
        return chromosome

    def run(self):
        population = self.generate_initial_population()
        best_overall_chromosome = None
        best_overall_fitness = float('inf')

        for gen in range(self.generations):
            fitnesses = [self.calculate_fitness(ind) for ind in population]
            
            # Elitisme
            sorted_indices = sorted(range(len(fitnesses)), key=lambda k: fitnesses[k])
            new_population = [population[i][:] for i in sorted_indices[:self.elitism_count]]
            
            if fitnesses[sorted_indices[0]] < best_overall_fitness:
                best_overall_fitness = fitnesses[sorted_indices[0]]
                best_overall_chromosome = population[sorted_indices[0]][:]

            while len(new_population) < self.pop_size:
                p1 = self.selection_roulette(population, fitnesses)
                p2 = self.selection_roulette(population, fitnesses)
                
                c1, c2 = self.crossover(p1, p2)
                
                new_population.append(self.mutate(c1))
                if len(new_population) < self.pop_size:
                    new_population.append(self.mutate(c2))
            
            population = new_population

        return best_overall_chromosome, best_overall_fitness

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ag.py <instance_file>")
        sys.exit(1)
        
    instance_file = sys.argv[1]
    n, m, p = load_instance(instance_file)
    
    start_time = time.time()
    ga = GeneticAlgorithm(n, m, p)
    best_sol, best_fit = ga.run()
    end_time = time.time()
    
    print(f"Meilleur Makespan trouvé: {best_fit}")
    print(f"Temps de calcul: {end_time - start_time:.4f} secondes")
    # print(f"Solution: {best_sol}")
