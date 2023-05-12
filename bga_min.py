import random
import math
# Constants-Parameters of the BGA
GENE1 = 10    # length of binary substring for decision variable 1
GENE2 = 10    # length of binary substring for decision variable 2
N = 500       # size of population 200
T = 200       # max number of generations
# UB = 10.0      # upper bound (same for both decision variables) for rosenbrock [1,1] result must be 0
# LB = -10.0     # lower bound (same for both decision variables) for rosenbrock
UB = 5.12  # rasting function [0,0] result must be 0
LB = -5.12
PC = 0.9      # probability of crossover
PM = 0.2      # probability of mutation

# Data Structure of Chromosome


class Chromosome:

    '''
    This class represents a single chromosome in the population. 
    The constructor initializes the binary string, decision variable values, real-coded variable values, and fitness. 
    It has no time or space complexity.
    The time complexity of this class is O(1) as it initializes the attributes with their default values. 
    The space complexity of this class is O(1).
    '''

    def __init__(self, binaryString=None, dv1=None, dv2=None, x1=None, x2=None, fitness=None):
        self.binaryString = binaryString if binaryString is not None else ''
        self.dv1 = dv1 if dv1 is not None else 0
        self.dv2 = dv2 if dv2 is not None else 0
        self.x1 = x1 if x1 is not None else 0
        self.x2 = x2 if x2 is not None else 0
        self.fitness = fitness if fitness is not None else 0


# Utility to compare chromosomes in terms of their fitness (for sorting function)
def compareChroms(obj1, obj2):
    '''
    This utility function takes in two chromosomes and returns True if the fitness of the first chromosome is less than that of the second chromosome. 
    It is used for sorting the population.
    The time complexity of this function is O(1) as it compares the fitness values of two chromosomes. 
    The space complexity of this function is O(1).
    '''
    return obj1.fitness < obj2.fitness


# Function to decode the value of a given string, from index 'start' to index 'end'
def decodeValue(str, start, end):
    '''
    This function takes in a binary string, start index, and end index and returns the decimal value of the substring of the binary string from start index to end index. 
    The time complexity of this function is O(n) where n is the length of the substring.
    The space complexity is O(1).
    '''
    ans = 0
    exp = 0
    for i in range(end, start - 1, -1):
        if str[i] == '1':
            ans += int(math.pow(2, exp))
        exp += 1
    return ans

# Scaling function to transform the decimal value of a binary string into a real coded value based on bounds


def scalingFunction(dv, length):
    '''
    This function takes in a decimal value (dv) and length and returns a real-coded value based on the upper and lower bounds. 
    The time complexity of this function is O(1) and the space complexity is O(1).
    '''
    p = (UB - LB) / (math.pow(2, length) - 1.0)
    return LB + p * dv

# Initialize a random chromosome as a binary string


def initializeRandomIndividual():
    '''
     This function initializes a single random chromosome as a binary string.
     The time complexity of this function is O(GENE1 + GENE2) where GENE1 and GENE2 are the lengths of binary substrings for decision variables 1 and 2 respectively. 
     The space complexity is also O(1). because it creates and returns only one chromosome object at a time, regardless of the value of GENE1 and GENE2. 
    '''
    binaryString = ''
    for i in range(GENE1 + GENE2):
        r = random.randint(0, 1)
        if r == 1:
            binaryString += '1'
        else:
            binaryString += '0'
    return Chromosome(binaryString)

# Initialize the entire population of individuals


def initializeRandomPop(pop):
    '''
     This function initializes the entire population of individuals. 
     It takes in a list of chromosomes and initializes each chromosome in the list by calling the initializeRandomIndividual function. 
     The time complexity of this function is O(N * (GENE1 + GENE2)) where N is the size of the population. 
     The space complexity is also O(N * (GENE1 + GENE2)). So O(N).
    '''
    for i in range(N):
        pop.append(initializeRandomIndividual())


# Evaluate a single chromosome
def evaluate(chrom):
    '''
    This function evaluates a single chromosome. It decodes the values of decision variables and calculates the fitness based on the rastrigin function. If an individual violates the upper or lower bounds, a penalty is applied. 
    The time complexity of this function is O(GENE1 + GENE2) and the space complexity is O(1).
    '''
    # Values of decision variables are codified at this stage
    chrom.dv1 = decodeValue(chrom.binaryString, 0, GENE1-1)
    chrom.dv2 = decodeValue(chrom.binaryString, GENE1, GENE1+GENE2-1)
    chrom.x1 = scalingFunction(chrom.dv1, GENE1)
    chrom.x2 = scalingFunction(chrom.dv2, GENE2)
    '''
    if chrom.x1 < -20 or chrom.x1 > 20 or chrom.x2 < -20 or chrom.x2 > 20:
        # Apply death penalty
        chrom.fitness = -1000
    '''
    # f an individual violates the upper or lower bounds of the problem, a penalty is applied that is equal to the sum of the differences between the individual's position and the nearest bound for each dimension. The penalty reduces the fitness of the individual, making it less likely to be selected for reproduction, but it does not completely disqualify the individual.
    # Check if individual violates bounds
    if chrom.x1 < LB or chrom.x1 > UB or chrom.x2 < LB or chrom.x2 > UB:
        # Apply a penalty function linear penalty function
        penalty = max(0, abs(chrom.x1 - LB)) + max(0, abs(chrom.x1 - UB)) + \
            max(0, abs(chrom.x2 - LB)) + max(0, abs(chrom.x2 - UB))
        chrom.fitness -= penalty
    else:
        # Calculate fitness from the objective function
        chrom.fitness = 10 * 2 + (chrom.x1 ** 2 - 10 * math.cos(2 * math.pi * chrom.x1)) + \
            (chrom.x2 ** 2 - 10 * math.cos(2 * math.pi * chrom.x2))  # rastring function


'''
For example, let's say the lower bound (LB) and upper bound (UB) for both decision variables are set to -10 and 10, respectively. If an individual has a position of (12, 8) in the search space, it violates the upper bound for the first dimension and the fitness will be penalized. The penalty for this individual would be:

penalty = max(0, abs(12 - 10)) + max(0, abs(8 - 10)) = 4
'''


# Binary Tournament Selection operator
def selection(pop):
    '''
    This function performs binary tournament selection.
    It takes in the population as a list of chromosomes and returns the mating pool as a list of chromosomes.
    The time complexity of this function is O(N) where N is the size of the population. The space complexity is O(N).
    '''
    matingPool = []
    for i in range(N):
        # Select two individuals randomly
        index1 = random.randint(0, N-1)
        index2 = random.randint(0, N-1)

        # Select the one with highest fitness
        if pop[index1].fitness > pop[index2].fitness:
            matingPool.append(pop[index1])
        else:
            matingPool.append(pop[index2])

    return matingPool


def crossover(matingPool):
    '''
    function performs crossover between pairs of parents in the mating pool to generate new offspring. 
    The time complexity of this function is O(N*(GENE1+GENE2)) where N is the size of the mating pool. 
    The space complexity is O(N).
    '''

    offspring = []
    for i in range(0, N-1, 2):
        # Randomly decide whether to apply crossover
        if random.uniform(0, 1) < PC:
            # Select the two parents
            parent1 = matingPool[i]
            parent2 = matingPool[i+1]

            # Select a random crossover point
            crossPoint = random.randint(1, GENE1+GENE2-1)

            # Generate two new offspring
            offspring1 = Chromosome()
            offspring2 = Chromosome()
            offspring1.binaryString = parent1.binaryString[:crossPoint] + \
                parent2.binaryString[crossPoint:]
            offspring2.binaryString = parent2.binaryString[:crossPoint] + \
                parent1.binaryString[crossPoint:]

            # Add the new offspring to the list
            offspring.append(offspring1)
            offspring.append(offspring2)
        else:
            # If no crossover, add the parents to the offspring list
            offspring.append(matingPool[i])
            offspring.append(matingPool[i+1])

    return offspring


def mutation(offspring):
    '''
    function applies mutation to the offspring generated through crossover. 
    The time complexity of this function is O(N * (GENE1+GENE2)), where N is the size of the population and GENE1+GENE2 is the length of each chromosome. 
    The space complexity is O(1) since the function mutates the chromosomes in-place without creating any new data structures.
    '''
    for i in range(N):
        for j in range(GENE1 + GENE2):
            # Randomly decide whether to apply mutation
            if random.uniform(0, 1) < PM:
                # Flip the bit
                if offspring[i].binaryString[j] == '1':
                    offspring[i].binaryString = offspring[i].binaryString[:j] + \
                        '0' + offspring[i].binaryString[j+1:]
                else:
                    offspring[i].binaryString = offspring[i].binaryString[:j] + \
                        '1' + offspring[i].binaryString[j+1:]
                # Evaluate the fitness of the new offspring
                evaluate(offspring[i])


def runBGA():
    '''
     function is the main function that runs the Binary Genetic Algorithm. 
     It initializes the population, evaluates the fitness of the initial population,
      performs selection, crossover, and mutation on the offspring, evaluates the fitness 
      of the new offspring, combines the parent and offspring populations, and removes
      the weakest individuals. It returns the best individual of the final population. 
      The time complexity of the runBGA() function is O(T * N * (N + GENE1 + GENE2)) where T is the number of generations, N is the population size, and GENE1 and GENE2 are the lengths of the binary strings representing the two genes.
     The space complexity of the function is O(N * (GENE1 + GENE2)) as we need to store the population and their binary strings.
    '''
    # Initialize population
    pop = []
    initializeRandomPop(pop)

    # Evaluate the fitness of the initial population
    for i in range(N):
        evaluate(pop[i])

    # Sort the population by fitness
    pop.sort(key=lambda x: x.fitness)

    # Print the best individual of the initial population
    print(
        f"Generation 0: Best fitness = {pop[0].fitness}, Best solution = ({pop[0].x1}, {pop[0].x2})")

    # Repeat for T generations
    for t in range(1, T+1):
        # Select individuals from the current population
        matingPool = selection(pop)

        # Generate new offspring using crossover
        offspring = crossover(matingPool)

        # Mutate the new offspring
        mutation(offspring)

        # Evaluate the fitness of the new offspring
        for i in range(len(offspring)):
            evaluate(offspring[i])

        # Combine the parent and offspring populations
        pop += offspring

        # Sort the combined population by fitness
        pop.sort(key=lambda x: x.fitness)

        # Remove the weakest individuals
        pop = pop[:N]

        # Print the best individual of the current population
        print(
            f"Generation {t}: Best fitness = {pop[0].fitness}, Best solution = ({pop[0].x1}, {pop[0].x2})")

    # Return the best individual of the final population
    return pop[0]


if __name__ == '__main__':
    runBGA()
