'''
This project solves minimize the Rastrigin Function problem with Binary Coded Genetic Algorithm.
Rastrigin function's minimize solution is 0 at [0,0]. 
@ Sena Kılınç 20191701033
'''

import random
import math

# Constants-Parameters of the BGA
GENE1 = 10    # length of binary substring for decision variable 1
GENE2 = 10    # length of binary substring for decision variable 2
N = 500       # size of population 
T = 200       # max number of generations
UB = 5.12     # Rastrigin function upper bound
LB = -5.12    # Rastrigin function lower bound
PC = 0.9      # probability of crossover
PM = 0.2      # probability of mutation


class Chromosome:

    '''
    This class represents a single chromosome in the population. 
    '''
    def __init__(self, binaryString=None, dv1=None, dv2=None, x1=None, x2=None, fitness=None):
        '''
        The constructor initializes the binary string, decision variable values, real-coded variable values, and fitness. 
        It has no time or space complexity.
        Time complexity: O(1) - Constant. 
        Space complexity: O(1) - Constant. 
        '''
        self.binaryString = binaryString if binaryString is not None else ''  # Binary string representation
        self.dv1 = dv1 if dv1 is not None else 0 # Decoded value of gene 1
        self.dv2 = dv2 if dv2 is not None else 0 # Decoded value of gene 2
        self.x1 = x1 if x1 is not None else 0 # Scaled value of gene 1
        self.x2 = x2 if x2 is not None else 0 # Scaled value of gene 2
        self.fitness = fitness if fitness is not None else 0 # Fitness value


def compareChroms(obj1, obj2):
    '''
    This function takes in two chromosomes and returns True if the fitness of the first chromosome is less than the second chromosome. 
    It is used for sorting the population.
    Time complexity: O(1) - Constant. 
    Space complexity: O(1) - Constant. 
    '''
    return obj1.fitness < obj2.fitness # Comparison function for sorting chromosomes based on fitness

def decodeValue(str, start, end):
    '''
    This function takes in a binary string, start index, and end index and returns the decimal value of the substring of the binary string from start index to end index. 
    Time complexity: O(end - start + 1) - Linear. 
    Space complexity: O(1) - Constant. 
    '''
    ans = 0 # Initialize the variable to hold the decoded decimal value
    exp = 0 # Initialize the exponent value for computing the decimal value
    for i in range(end, start - 1, -1):  # Iterate over the range of indices in reverse order
        if str[i] == '1': # If the bit at the current index is '1'
            ans += int(math.pow(2, exp))  # Add the corresponding decimal value to ans using exponentiation
        exp += 1  # Increment the exponent value for the next iteration
    return ans  # Return the decoded decimal value

def scalingFunction(dv, length):
    '''
    This function takes in a decimal value (dv) and length and returns a real-coded value based on the upper and lower bounds. 
    Time complexity: O(1) - Constant. 
    Space complexity: O(1) - Constant.
    '''
    p = (UB - LB) / (math.pow(2, length) - 1.0)  # Calculate the scaling factor based on the upper bound, lower bound, and gene length
    return LB + p * dv # Scale the decoded value using the scaling factor and add the lower bound to obtain the scaled value within the specified range


def initializeRandomIndividual():
    '''
    This function initializes a single random chromosome as a binary string.
    Time complexity: O(GENE1 + GENE2) - Linear. 
    Space complexity: O(1) - Constant. 
    '''
    binaryString = '' # Initialize an empty binary string
    for i in range(GENE1 + GENE2): # sum lengths of binary substrings
        r = random.randint(0, 1) # Generate a binary string by randomly choosing 0 or 1 for each gene
        if r == 1:
            binaryString += '1'
        else:
            binaryString += '0'
    return Chromosome(binaryString) # Create a new Chromosome object with the generated binary string

def initializeRandomPop(pop):
    '''
    This function initializes the entire population of individuals. 
    It takes in a list of chromosomes and initializes each chromosome in the list by calling the initializeRandomIndividual function. 
    Time complexity: O(N * (GENE1 + GENE2)) - Linear. 
    Space complexity: O(N) - Linear. 
    '''
    for i in range(N):
        pop.append(initializeRandomIndividual()) # Add a random individual to the population

def evaluate(chrom):
    '''
    This function evaluates a single chromosome. It decodes the values of decision variables and calculates the fitness based on the Rastrigin function. 
    If an individual violates the upper or lower bounds, a penalty is applied. 
    Time complexity: O(1) - Constant. 
    Space complexity: O(1) - Constant.
    '''
    chrom.dv1 = decodeValue(chrom.binaryString, 0, GENE1-1)  # Decode gene 1's binary string to decimal value
    chrom.dv2 = decodeValue(chrom.binaryString, GENE1, GENE1+GENE2-1) # Decode gene 2's binary string to decimal value
    chrom.x1 = scalingFunction(chrom.dv1, GENE1) # Scale gene 1's decoded value
    chrom.x2 = scalingFunction(chrom.dv2, GENE2) # Scale gene 2's decoded value

    if chrom.x1 < LB or chrom.x1 > UB or chrom.x2 < LB or chrom.x2 > UB: # If an individual violates the upper or lower bounds of the problem
        # Apply a linear penalty which is equal to the sum of the differences between the individual's position and the nearest bound for each dimension. 
        penalty = max(0, abs(chrom.x1 - LB)) + max(0, abs(chrom.x1 - UB)) + max(0, abs(chrom.x2 - LB)) + max(0, abs(chrom.x2 - UB))
        chrom.fitness -= penalty # The penalty reduces the fitness of the individual, making it less likely to be selected for reproduction, but it does not completely disqualify the individual.

    else:
        # Calculate the fitness from the objective function
        chrom.fitness = 10 * 2 + (chrom.x1 ** 2 - 10 * math.cos(2 * math.pi * chrom.x1)) + (chrom.x2 ** 2 - 10 * math.cos(2 * math.pi * chrom.x2))  # Rastrigin function

def selection(pop):
    '''
    This function performs binary tournament selection.
    It takes in the population as a list of chromosomes and returns the mating pool as a list of chromosomes.
    Time complexity: O(N) - Linear. 
    Space complexity: O(N) - Linear.
    '''
    matingPool = [] # Initialize an empty mating pool
    for i in range(N):  # Iterate over the range of population
        # Select two individuals randomly
        index1 = random.randint(0, N-1) # Generate a random index between 0 and N-1
        index2 = random.randint(0, N-1) # Generate another random index between 0 and N-1

        # Select the one with highest fitness
        if pop[index1].fitness > pop[index2].fitness:
            matingPool.append(pop[index1]) # Add the individual to the mating pool
        else:
            matingPool.append(pop[index2]) # Add the individual to the mating pool
    return matingPool # Return the generated mating pool


def crossover(matingPool):
    '''
    This function performs crossover between pairs of parents in the mating pool to generate new offspring. 
    Time complexity: O(N) - Linear. 
    Space complexity: O(N) - Linear.
    '''
    offspring = []  # Initialize an empty offspring list
    for i in range(0, N-1, 2): # Iterate over the mating pool by pairs
        if random.uniform(0, 1) < PC: # Randomly decide whether to apply crossover
            # Select the two parents
            parent1 = matingPool[i]
            parent2 = matingPool[i+1]

            # Select a random crossover point
            crossPoint = random.randint(1, GENE1+GENE2-1)

            # Generate two new offspring
            offspring1 = Chromosome()
            offspring2 = Chromosome()
            # Perform crossover by combining genes from parents
            offspring1.binaryString = parent1.binaryString[:crossPoint] + parent2.binaryString[crossPoint:]
            offspring2.binaryString = parent2.binaryString[:crossPoint] + parent1.binaryString[crossPoint:]

            # Add the new offspring to the list
            offspring.append(offspring1)
            offspring.append(offspring2)
        else:
            # If crossover probability is not met, add the parents to the offspring list
            offspring.append(matingPool[i])
            offspring.append(matingPool[i+1])

    return offspring # Return the list of offspring chromosomes

def mutation(offspring):
    '''
    This function applies mutation to the offspring generated through crossover. 
    Time complexity: O(N * (GENE1 + GENE2)) - Linear. 
    Space complexity: O(1) - Constant.
    '''
    for i in range(N): # Iterate over the offspring
        for j in range(GENE1 + GENE2): # Iterate over the genes in the chromosome
            # Randomly decide whether to apply mutation
            if random.uniform(0, 1) < PM:
                if offspring[i].binaryString[j] == '1': # If the gene is '1', Flip the gene to '0'
                    offspring[i].binaryString = offspring[i].binaryString[:j] + '0' + offspring[i].binaryString[j+1:]
                else: # If the gene is '0', Flip the gene to '1'
                    offspring[i].binaryString = offspring[i].binaryString[:j] + '1' + offspring[i].binaryString[j+1:]
                # Evaluate the fitness of the new offspring
                evaluate(offspring[i]) # Recalculate the fitness of the mutated chromosome

def get_fitness(chrom):
    '''
    Returns the fitness value of the chromosome
    Time complexity: O(1) - Constant. 
    Space complexity: O(1) - Constant.
    '''
    return chrom.fitness

def runBGA():
    '''
    This function is the main function that runs the Binary Genetic Algorithm. 
    It initializes the population, evaluates the fitness of the initial population,
    performs selection, crossover, and mutation on the offspring, evaluates the fitness 
    of the new offspring, combines the parent and offspring populations, and removes
    the weakest individuals. It returns the best individual of the final population. 
    Time complexity: O(T * N * (GENE1 + GENE2)) - Quadratic. 
    Space complexity: (O(N)) - Linear.
    '''
    # Initialize population
    pop = []
    initializeRandomPop(pop)

    # Evaluate the fitness of the initial population
    for i in range(N):
        evaluate(pop[i])

    # Sort the population by fitness
    pop.sort(key=get_fitness)

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
        pop.sort(key=get_fitness)


        # Remove the weakest individuals
        pop = pop[:N]

        # Print the best individual of the current population
        print(
            f"Generation {t}: Best fitness = {pop[0].fitness}, Best solution = ({pop[0].x1}, {pop[0].x2})")

    # Return the best individual of the final population
    return pop[0]


if __name__ == '__main__':
    runBGA()  # Rastrigin function's minimize solution is 0 at [0,0].
