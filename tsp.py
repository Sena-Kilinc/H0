import numpy as np
import random


class TSP:
    def __init__(self, num_cities, pop_size, num_generations):
        self.num_cities = num_cities
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.cities = np.random.randint(50, size=(num_cities, 2))
        self.population = np.zeros((pop_size, num_cities))
        self.fitness = np.zeros(pop_size)
        self.best_distance = np.inf
        self.best_route = np.zeros(num_cities)

    def generate_population(self):
        for i in range(self.pop_size):
            route = np.arange(self.num_cities)
            np.random.shuffle(route)
            self.population[i] = route

    def calculate_fitness(self, route):
        distance = 0
        for i in range(self.num_cities-1):
            index1, index2 = int(route[i]), int(route[i+1])
            city1, city2 = self.cities[index1], self.cities[index2]
            distance += np.sqrt((city2[0] - city1[0])
                                ** 2 + (city2[1] - city1[1])**2)
        return 1/distance

    def evaluate_population(self):
        for i in range(self.pop_size):
            self.fitness[i] = self.calculate_fitness(self.population[i])
        max_index = np.argmax(self.fitness)
        if self.fitness[max_index] > 1/self.best_distance:
            self.best_distance = 1/self.fitness[max_index]
            self.best_route = self.population[max_index]

    def crossover(self, parent1, parent2):
        child = np.zeros(self.num_cities)
        start, end = random.sample(range(self.num_cities), 2)
        if start > end:
            start, end = end, start
        for i in range(start, end+1):
            child[i] = parent1[i]
        for i in range(self.num_cities):
            if parent2[i] not in child:
                for j in range(self.num_cities):
                    if child[j] == 0:
                        child[j] = parent2[i]
                        break
        return child

    def mutate(self, child):
        index1, index2 = random.sample(range(self.num_cities), 2)
        child[index1], child[index2] = child[index2], child[index1]
        return child

    def generate_new_population(self):
        new_population = np.zeros((self.pop_size, self.num_cities))
        for i in range(self.pop_size):
            parent1, parent2 = random.sample(list(self.population), 2)
            child = self.crossover(parent1, parent2)
            if random.uniform(0, 1) < 0.2:
                child = self.mutate(child)
            new_population[i] = child
        self.population = new_population

    def solve(self):
        self.generate_population()
        for i in range(self.num_generations):
            self.evaluate_population()
            self.generate_new_population()
            print("Generation: ", i, " Best Distance: ", self.best_distance)
        print("Best Route: ", self.best_route,
              " Best Distance: ", self.best_distance)


tsp = TSP(num_cities=20, pop_size=400, num_generations=500)
tsp.solve()
