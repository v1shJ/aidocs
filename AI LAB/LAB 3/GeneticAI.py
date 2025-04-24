import random

# Define parameters
POPULATION_SIZE = 10
MUTATION_RATE = 0.2  # 20% chance of mutation
GENERATIONS = 200

# Define the equation a + 2b + 3c + 4d = 30
def fitness(chromosome):
    a, b, c, d = chromosome
    return abs((a + 2*b + 3*c + 4*d) - 30)  # Lower fitness is better

# Generate a random chromosome (solution candidate)
def generate_chromosome():
    return [random.randint(0, 10) for _ in range(4)]  # a, b, c, d values

# Generate initial population
def generate_population():
    population = [generate_chromosome() for _ in range(POPULATION_SIZE)]
    print("\nInitial Population:")
    for idx, chromo in enumerate(population):
        print(f"Chromosome {idx+1}: {chromo}, Fitness: {fitness(chromo)}")
    return population

# Selection: Choose the best two parents
def select_parents(population):
    sorted_population = sorted(population, key=fitness)
    parent1, parent2 = sorted_population[:2]
    print(f"\nSelected Parents for Crossover:\nParent 1: {parent1}, Fitness: {fitness(parent1)}\nParent 2: {parent2}, Fitness: {fitness(parent2)}")
    return parent1, parent2

# Crossover: Create offspring by mixing two parents
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)  # Pick crossover point (1 to len-1)

    # Creating two children by swapping genes after crossover point
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    print(f"\nCrossover at index {crossover_point}:")
    print(f"Child 1: {child1}")
    print(f"Child 2: {child2}")

    return child1, child2

# Mutation: Randomly alter a gene
def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        index = random.randint(0, 3)
        old_value = chromosome[index]
        chromosome[index] = random.randint(0, 10)
        print(f"Mutation occurred at index {index}: {old_value} → {chromosome[index]}")
    return chromosome

# Genetic Algorithm Execution
def genetic_algorithm():
    population = generate_population()
    
    for generation in range(GENERATIONS):
        print(f"\n\n===== Generation {generation+1} =====")
        
        population = sorted(population, key=fitness)
        
        # Check if we found an exact solution
        if fitness(population[0]) == 0:
            print(f"\nSolution found in generation {generation+1}: {population[0]}")
            return population[0]
        
        # Select parents
        parent1, parent2 = select_parents(population)
        
        # Create next generation
        new_population = [parent1, parent2]  # Keep best solutions
        
        while len(new_population) < POPULATION_SIZE:
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.append(child1)
            new_population.append(child2)
        
        population = new_population[:POPULATION_SIZE]  # Maintain population size
        
        # Print population for this generation
        print("\nNew Population:")
        for idx, chromo in enumerate(population):
            print(f"Chromosome {idx+1}: {chromo}, Fitness: {fitness(chromo)}")

    print("\nNo exact solution found.")
    return None

# Run the algorithm
solution = genetic_algorithm()
print("\nFinal Solution:", solution)
