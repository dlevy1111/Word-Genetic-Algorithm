import random


def main():
    string_to_guess = "all that glitters is not gold"
    size_of_string = len(string_to_guess)
    population = Population(500, 0.0001, size_of_string)  # mutation rate is as a decimal, for example, 0.2

    string_to_guess_value = 0
    for letter in string_to_guess:
        string_to_guess_value = string_to_guess_value + ord(letter)

    timer = 0
    generation = 0
    while True:  # looping section, press cmd + c to end the program
        timer = timer + 1

        if population.end_program():
            print(f"The string to guess was {string_to_guess}, and it took {generation} generations.")
            break

        if timer % 20000 == 0:  # just before the population is recreated
            print(string_to_guess)  # the program happens a lot faster if you lower ^ number and the number below
            population.compute_fitness(string_to_guess)
            population.live()
            print(f"This is generation {generation}")

            print()

        if timer > 25000:  # the population is recreated
            population.make_mating_pool()  # ^ this number
            population.reproduce()
            timer = 0
            generation = generation + 1


class DNA:
    def __init__(self, size):  # creating DNA
        self.genes = []
        self.size = size
        for i in range(0, size):
            if random.randint(0, 26) <= 1:
                self.genes.append(" ")
            else:
                self.genes.append(chr(random.randint(97, 122)))

    def breed(self, other):
        mother = self
        father = other
        child = DNA(self.size)
        for i in range(0, len(self.genes)):
            if random.randint(0, 1) == 0:
                child.genes[i] = mother.genes[i]
            else:
                child.genes[i] = father.genes[i]
        return child

    def mutate(self, mutation_rate):
        mutation_rate = mutation_rate*100
        for i in range(0, len(self.genes)):
            if random.randint(0, 100) <= mutation_rate:
                self.genes[i] = chr(random.randint(97, 122))

    def __str__(self):
        temp_str = ""
        for i in range(0, len(self.genes)):
            temp_str = temp_str + self.genes[i]
        return temp_str


class String:
    def __init__(self, size):
        self.dna = DNA(size)
        self.fitness = 0

    def print(self):
        print("".join(self.dna.genes))
        print("Fitness = "+str(self.fitness))

  # the big work-horse of the program
class Population:
    def __init__(self, population_size, mutation_rate, string_length):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.organisms = []
        self.mating_pool = []
        self.string_length = string_length  # saving the overall string's length
        for i in range(0, self.population_size):
            self.organisms.append(String(string_length))

    def compute_fitness(self, string_to_guess):
        for organism in self.organisms:
            similar_letters = 0
            for i in range(0, len(organism.dna.genes)):
                if organism.dna.genes[i] == string_to_guess[i]:
                    similar_letters = similar_letters + 1
            organism.fitness = (similar_letters/len(string_to_guess))**1

    def make_mating_pool(self):
        self.mating_pool.clear()
        min_fitness = self.organisms[0].fitness
        max_fitness = self.organisms[0].fitness
        for organism in self.organisms:
            if organism.fitness < min_fitness:
                min_fitness = organism.fitness
            if organism.fitness > max_fitness:
                max_fitness = organism.fitness

        for organism in self.organisms:
            mating_amount = organism.fitness*120-20  # range is (-20,100)
            for i in range(-10, int(mating_amount)):
                self.mating_pool.append(organism)

    def reproduce(self):
        self.organisms.clear()
        for i in range(0, self.population_size):
            # print("mating pool size: "+str(len(self.mating_pool)))
            mother = self.mating_pool[random.randint(0, len(self.mating_pool)-1)]
            father = self.mating_pool[random.randint(0, len(self.mating_pool)-1)]
            child = String(self.string_length)
            child.dna = mother.dna.breed(father.dna)
            child.dna.mutate(self.mutation_rate)
            self.organisms.append(child)

    def live(self):
        max_fitness_organism = self.organisms[0]
        for organism in self.organisms:
            if organism.fitness > max_fitness_organism.fitness:
                max_fitness_organism = organism
        max_fitness_organism.print()

    def best_fitness(self):
        max_fitness_organism = self.organisms[0]
        for organism in self.organisms:
            if organism.fitness > max_fitness_organism.fitness:
                max_fitness_organism = organism
        return max_fitness_organism

    def end_program(self):
        if self.best_fitness().fitness == 1.0:
            return True
        else:
            return False


main()
