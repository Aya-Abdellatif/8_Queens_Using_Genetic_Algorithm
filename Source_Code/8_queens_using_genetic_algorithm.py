#imports
import random

#Problem Parameters
NUM_QUEENS = 8
POPULATION_SIZE = 100 
MUTATION_RATE = 0.1 
MAX_FITNESS = 28  #NUM_QUEENS *(NUM_QUEENS-1)/2


def CreateBoard():
    return [random.randint(0, NUM_QUEENS - 1) for _ in range(NUM_QUEENS)]


#Fitness function
def Fitness(board):
    clashes = 0 
    for i in range(NUM_QUEENS):
        r = board[i]
        for j in range(NUM_QUEENS):
            if i != j:
                d = abs(i - j)
                if board[j] in [r, r - d, r + d]:
                    clashes += 1
    return MAX_FITNESS - clashes #28 - clashes

#wheel_selection
def Selection(population):
    selected_population = [] 

    fitness_values = [Fitness(board) for board in population]
    total_fitness = sum(fitness_values)

    normalized_fitness = [each / total_fitness for each in fitness_values]

    for _ in range(POPULATION_SIZE):
        value = random.random()
        probability_sum = 0
        for i in range(POPULATION_SIZE):
            probability_sum += normalized_fitness[i]
            if probability_sum >= value:
                selected_population.append(population[i])
                break

    return selected_population

def Crossover(parent1, parent2):
    crossover_point = random.randint(1, NUM_QUEENS - 1) #RANDOM POINT
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2


def Mutation(board):
    if random.random() < MUTATION_RATE:
        gene_to_mutate = random.randint(0, NUM_QUEENS - 1)
        new_value = random.randint(0, NUM_QUEENS - 1)
        while new_value == board[gene_to_mutate]:
            new_value = random.randint(0, NUM_QUEENS - 1)
        board[gene_to_mutate] = new_value

        return board
    

def PrintChessBoard(board):
  
  for row in range(NUM_QUEENS -1, -1, -1):
    for col in range(NUM_QUEENS):
        if board[col] == row:
            print("Q", end=" ")
        else:
            print("-", end=" ")  
    print()

#Genetic algorith
def GeneticAlgorithm(num_of_generations):
    population = [CreateBoard() for _ in range(POPULATION_SIZE)] 
    best_fitness = 0
    best_board = None
    for generation in range(num_of_generations):
        #selection
        selected = Selection(population)

        #crossover
        children = []
        for i in range(0, POPULATION_SIZE, 2):
            parent1 = selected[i]
            parent2 = selected[i+1]
            child1, child2 = Crossover(parent1, parent2)
            children.append(child1)
            children.append(child2)
            

        #Mutation
        for child in children:
            Mutation(child)


        population = children # new population

        #update best solution
        current_fitness = max(Fitness(board) for board in population)
        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_board = max(population, key = Fitness)

        #print progress
        print(f'\rGeneration: {generation + 1}, best fitness: {best_fitness}', end = '')
        if current_fitness == MAX_FITNESS: #28
            break

    #print solution
    if(best_fitness != MAX_FITNESS):
        print("\nNO OPTIMAL SOLUTION FOUND")
    else:
        print(f"\nOPTIMAL SOLUTION FOUND IN {generation + 1} GENERATIONS: ")
        print(f"BOARD: {best_board}")
        print(f"FITNESS: {best_fitness}") #28
        print('===================================================')
        PrintChessBoard(best_board)


if __name__ == "__main__":
    print('===================================================')
    num_of_generations = int(input("Enter the number of Generations: "))
    print('===================================================')
    GeneticAlgorithm(num_of_generations)