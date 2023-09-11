import random


class Genome:
    """
    A class for generating genomes and populations.

    Attributes:
        limits (list): A list of integer limits for genome generation.

    Methods:
        make_genome(): Generates a single genome based on the specified limits.
        make_population(size): Generates a population of genomes with the given size.
    """

    def __init__(self, limits):
        """
        Initializes a Genome object with the provided limits.

        Args:
            limits (list): A list of integer limits for genome generation.
        """
        self.limits = limits

    def make_genome(self):
        """
        Generates a single genome based on the specified limits.

        Returns:
            list: A list representing the generated genome.
        """
        return [random.randint(0, gen) for gen in self.limits]

    def make_population(self, size):
        """
        Generates a population of genomes with the given size.

        Args:
            size (int): The size of the population to generate.

        Returns:
            list: A list of lists representing the generated population.
        """
        return [self.make_genome() for _ in range(size)]


class Mutation:
    """
    A class for applying mutations to genomes.
    """

    def __init__(self, genome, limits):
        """
        Initializes a Mutation object with the genome and limits.

        Args:
            genome (list): The genome to be mutated.
            limits (list): A list of integer limits for mutation.
        """
        self.genome = genome
        self.limits = limits

    def make_linear_mutation(self):
        """
        Makes linear mutation to the genome.

        Returns:
            list: The mutated genome.
        """

        if len(self.limits) != len(self.genome):
            raise ValueError("Genome and limits must have the same length for mutation.")

        mutated_genome = self.genome.copy()

        index_a = random.randint(0, len(self.genome) - 1)
        index_b = random.randint(0, len(self.genome) - 1)

        # Mutate gene at index_a
        if random.random() < 0.5:  # 50% chance of incrementing
            mutated_genome[index_a] = min(mutated_genome[index_a] + 1, self.limits[index_a])
        else:  # 50% chance of decrementing
            mutated_genome[index_a] = max(mutated_genome[index_a] - 1, 0)

        # Mutate gene at index_b
        if random.random() < 0.5:  # 50% chance of incrementing
            mutated_genome[index_b] = min(mutated_genome[index_b] + 1, self.limits[index_b])
        else:  # 50% chance of decrementing
            mutated_genome[index_b] = max(mutated_genome[index_b] - 1, 0)

        return mutated_genome


class Crossover:
    """
    A class for performing crossover operations on genomes.
    """

    def __init__(self, genome_a, genome_b):
        """
        Initializes a Crossover object with two parent genomes.

        Args:
            genome_a (list): The first parent genome.
            genome_b (list): The second parent genome.
        """
        self.genome_a = genome_a
        self.genome_b = genome_b

    def single_point_crossover(self):
        """
        Performs single-point crossover on the parent genomes.

        Returns:
            tuple: Two offspring genomes.
        """

        if len(self.genome_a) != len(self.genome_b):
            raise ValueError("Parent genomes must have the same length for single-point crossover.")

        if len(self.genome_a) < 2:
            return self.genome_a, self.genome_b

        crossover_point = random.randint(0, len(self.genome_a) - 1)
        offspring_a = self.genome_a[:crossover_point] + self.genome_b[crossover_point:]
        offspring_b = self.genome_b[:crossover_point] + self.genome_a[crossover_point:]

        return offspring_a, offspring_b


class Population:
    """
    A class for managing populations of genomes.
    """

    def __init__(self, population):
        """
        Initializes a Population object with the initial population.

        Args:
            population (list): A list of genomes representing the initial population.
        """
        self.population = population

    @staticmethod
    def _temp_fitness(self, genome):
        return random.randint(1, 20)

    def get_first_two_items(self):
        return self.population[0:2]

    def select(self, fitness_function):
        """
        Selects two genomes from the population based on a fitness function.

        Args:
            fitness_function (callable): The fitness function used for selection.

        Returns:
            tuple: Two selected genomes.
        """
        return random.choices(
            population=self.population,
            weights=[fitness_function(genome=genome) for genome in self.population],
            k=2
        )


if __name__ == "__main__":
    print("Methods")
