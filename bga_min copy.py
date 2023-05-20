import random
import math
GENE1 = 10    
GENE2 = 10    
N = 500       
T = 200       
UB = 5.12  
LB = -5.12
PC = 0.9      
PM = 0.2      

class Chromosome:
    def __init__(self, binaryString=None, dv1=None, dv2=None, x1=None, x2=None, fitness=None):
        self.binaryString = binaryString if binaryString is not None else ''
        self.dv1 = dv1 if dv1 is not None else 0
        self.dv2 = dv2 if dv2 is not None else 0
        self.x1 = x1 if x1 is not None else 0
        self.x2 = x2 if x2 is not None else 0
        self.fitness = fitness if fitness is not None else 0

def compareChroms(obj1, obj2):
    return obj1.fitness < obj2.fitness

def decodeValue(str, start, end):
    ans = 0
    exp = 0
    for i in range(end, start - 1, -1):
        if str[i] == '1':
            ans += int(math.pow(2, exp))
        exp += 1
    return ans

def scalingFunction(dv, length):
    p = (UB - LB) / (math.pow(2, length) - 1.0)
    return LB + p * dv

def initializeRandomIndividual():
    binaryString = ''
    for i in range(GENE1 + GENE2):
        r = random.randint(0, 1)
        if r == 1:
            binaryString += '1'
        else:
            binaryString += '0'
    return Chromosome(binaryString)

def initializeRandomPop(pop):
    for i in range(N):
        pop.append(initializeRandomIndividual())


def evaluate(chrom):
    chrom.dv1 = decodeValue(chrom.binaryString, 0, GENE1-1)
    chrom.dv2 = decodeValue(chrom.binaryString, GENE1, GENE1+GENE2-1)
    chrom.x1 = scalingFunction(chrom.dv1, GENE1)
    chrom.x2 = scalingFunction(chrom.dv2, GENE2)

    if chrom.x1 < LB or chrom.x1 > UB or chrom.x2 < LB or chrom.x2 > UB:
        penalty = max(0, abs(chrom.x1 - LB)) + max(0, abs(chrom.x1 - UB)) + \
            max(0, abs(chrom.x2 - LB)) + max(0, abs(chrom.x2 - UB))
        chrom.fitness -= penalty
    else:
        chrom.fitness = 10 * 2 + (chrom.x1 ** 2 - 10 * math.cos(2 * math.pi * chrom.x1)) + \
            (chrom.x2 ** 2 - 10 * math.cos(2 * math.pi * chrom.x2))  # rastring function

def selection(pop):
    matingPool = []
    for i in range(N):
        index1 = random.randint(0, N-1)
        index2 = random.randint(0, N-1)

        if pop[index1].fitness > pop[index2].fitness:
            matingPool.append(pop[index1])
        else:
            matingPool.append(pop[index2])

    return matingPool

def crossover(matingPool):
    offspring = []
    for i in range(0, N-1, 2):
        if random.uniform(0, 1) < PC:
            parent1 = matingPool[i]
            parent2 = matingPool[i+1]
            crossPoint = random.randint(1, GENE1+GENE2-1)
            offspring1 = Chromosome()
            offspring2 = Chromosome()
            offspring1.binaryString = parent1.binaryString[:crossPoint] + \
                parent2.binaryString[crossPoint:]
            offspring2.binaryString = parent2.binaryString[:crossPoint] + \
                parent1.binaryString[crossPoint:]
            offspring.append(offspring1)
            offspring.append(offspring2)
        else:
            offspring.append(matingPool[i])
            offspring.append(matingPool[i+1])
    return offspring

def mutation(offspring):
    for i in range(N):
        for j in range(GENE1 + GENE2):
            if random.uniform(0, 1) < PM:
                if offspring[i].binaryString[j] == '1':
                    offspring[i].binaryString = offspring[i].binaryString[:j] + \
                        '0' + offspring[i].binaryString[j+1:]
                else:
                    offspring[i].binaryString = offspring[i].binaryString[:j] + \
                        '1' + offspring[i].binaryString[j+1:]
                evaluate(offspring[i])

def runBGA():
    pop = []
    initializeRandomPop(pop)
    for i in range(N):
        evaluate(pop[i])
    pop.sort(key=lambda x: x.fitness)
    print(
        f"Generation 0: Best fitness = {pop[0].fitness}, Best solution = ({pop[0].x1}, {pop[0].x2})")

    for t in range(1, T+1):
        matingPool = selection(pop)
        offspring = crossover(matingPool)
        mutation(offspring)
        for i in range(len(offspring)):
            evaluate(offspring[i])
        pop += offspring
        pop.sort(key=lambda x: x.fitness)
        pop = pop[:N]
        print(
            f"Generation {t}: Best fitness = {pop[0].fitness}, Best solution = ({pop[0].x1}, {pop[0].x2})")
    return pop[0]

if __name__ == '__main__':
    runBGA()
