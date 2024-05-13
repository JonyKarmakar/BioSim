import math
import random


# This module implements the Animals class to simulate the animals found on Rossumøya island.
# We have two subclasses, Herbivores and Carnivores that represent both type of animals and there are
# which represent their behaviors such as how they feed.
class Animal:
    """
       The Animals class.

       Attributes
       __________
       age
           *int*: Age of the animal.

       weight
           *float*: Weight of the animal.

       death
           *bool*: *True* if the animal dies, *False* otherwise.

       fitness
           *float*: Fitness of the animal.

       can_migrate
           *bool*: *True* if animal is likely to migrate to another cell, *False* otherwise.


       has_migrated
           *bool*: *True* if animal has migrated to another cell, *False* otherwise.
           Cannot be *True* if **can_migrate** is *False*.

       """

    parameters = {}
    min_weight=None
    def __init__(self, age=0, weight=None):
        self.age = age
        self.weight = weight
        self.offspring = False
        self.birth_count = 0
        self.fitness()
        self.death = False
        self.migrated = False
        #print("instance created")

    @classmethod
    def set_params(cls, params):
        """
        Set params for the animals.

        Parameters
        ----------
        params : dict
            Dictionary of *parameters* for each type of animal.
                """
        cls.parameters.update(params)

    def aging(self):
        """
        Increase Animal age by one year
        """
        self.age += 1
        #print("Age from aging in Animal:", self.age)
        return self.age

    def fitness(self):
        """
        Calculate fitness of the animal using the equation given
        """

        phi_age = self.parameters['phi_age']
        age_half = self.parameters['a_half']
        phi_weight = self.parameters['phi_weight']
        weight_half = self.parameters['w_half']
        #print('Age:', self.age)
        q_plus = 1 / (1 + math.exp(phi_age * (self.age - age_half)))
        q_minus = 1 / (1 + math.exp(-phi_weight * (self.weight - weight_half)))

        if self.weight <= 0:
            self.fitness_value = 0
        else:
            self.fitness_value = q_plus * q_minus


    def loss_of_weight(self):
        """
        Each year the weight of the animal is decreased by amount ηw
        """

        self.weight = self.weight - self.parameters['eta'] * self.weight
        self.fitness()
        return self.weight

    @classmethod
    def update_min_weight(cls):
        """
        Calculate the min weight using the formula ζ(wbirth + σbirth)
        """
        cls.min_weight = (cls.parameters['zeta']) * (
                cls.parameters['w_birth'] + cls.parameters['sigma_birth'])
        return cls.min_weight
    def birth(self, N):
        """
        This function takes the number of animals in a cell and return the offspring object,

         Parameters
        ----------
        N : int
            Number of animals of a species in a cell. Probability of giving birth is only
            calculated if there are at least two animals of the same species present in a cell.

        """

        mu = math.log((self.parameters['w_birth'] * self.parameters['w_birth']) / math.sqrt(
            (self.parameters['w_birth'] * self.parameters['w_birth']) + (
                    self.parameters['sigma_birth'] * self.parameters['sigma_birth'])))
        sigma = math.log(1 + (
                ((self.parameters['sigma_birth']) * (self.parameters['sigma_birth'])) / (
                (self.parameters['w_birth']) * (self.parameters['w_birth']))))
        offspring_weight = random.lognormvariate(mu, sigma)
        weight_loss = self.parameters['xi'] * offspring_weight

        if (weight_loss < self.weight):
            p_birth = min(1, self.parameters['gamma'] * self.fitness_value * (N -1))
            if (random.random() < p_birth):
                self.weight = self.weight - weight_loss
                self.fitness()
                self.birth_count = self.birth_count + 1
                return type(self)(age=0, weight=offspring_weight)
            else:
                return None
        else:
            return None



    def dies(self):
        """
        Compute probability of the animal dying and set ``death`` as *True*
        if probability is higher than a random threshold.
        """

        p_death = self.parameters['omega'] * (1 - self.fitness_value)
        if self.weight == 0 or random.random() < p_death:
            self.death = True
        return self.death

    def migration_probability(self):
        if self.migrated:
            return self.migrated
        else:
            p_migration = random.random() < self.parameters['mu'] * self.fitness_value
            #print("P Migration: ", p_migration)
            return p_migration


class Herbivores(Animal):

    """
    The 'Herbivore' animal type, is a subclass on animal calls and it feeds on fodder in
    lowland and highland. Herbivores eat in random order the amount *F* from the
    fodder available in the cell. Subsequently, its weight increases by: Beta * F
    """


    parameters = {'w_birth': 8,
                          'sigma_birth': 1.5,
                          'beta': 0.9,
                          'eta': 0.05,
                          'a_half': 40,
                          'phi_age': 0.6,
                          'w_half': 10,
                          'phi_weight': 0.1,
                          'mu': 0.25,
                          'gamma': 0.2,
                          'zeta': 3.5,
                  'xi': 1.2,
                  'omega': 0.4,
                  'F': 10
                  }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)
    def food(self, fodder):
        """
                Feeding function for herbivores.

        Returns **fodder**: the amount of food left in the cell after herbivore has eaten.

        Parameters
        ----------
        fodder : float
            The amount of food available in the cell.
        """
        if self.parameters['F'] <= fodder:
            fodder = fodder - self.parameters['F']
            self.weight = self.weight + self.parameters['beta'] * self.parameters['F']
            self.fitness()
        else:
            self.weight = self.weight + self.parameters['beta'] * fodder
            self.fitness()
            fodder = 0
        # print("Weight after eating:......", self.weight)
        return fodder

class Carnivores(Animal):
    """
        The 'Carnivre' animal type, is a subclass on animal calls and it feeds on herbivore.
        A carnivore continues to kills herbivores until it has eaten a specific amount or
        until it has tried to kill each herbivore present in the cell.
        """
    parameters = {'w_birth': 6,
                          'sigma_birth': 1.0,
                          'beta': 0.75,
                          'eta': 0.125,
                          'a_half': 40,
                          'phi_age': 0.3,
                          'w_half': 4,
                          'phi_weight': 0.4,
                          'mu': 0.4,
                          'gamma': 0.8,
                          'zeta': 3.5,
                          'xi': 1.1,
                          'omega': 0.8,
                          'F': 50,
                          'deltaPhiMax':10.0
                          }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)
    def feeds(self, h_pop):
        """
               Function for carnivores preying on herbivores.

               Parameters
               ----------
               h_pop : list
                   The list of herbivores present in the cell. The attribute **death** is set *True*
                   for each herbivores that is killed by the carnivore.
        """

        appetite = self.parameters['F']
        for herbivore in h_pop:
            if(herbivore.death is False):
                if self.fitness_value <= herbivore.fitness_value:
                    p_eating = 0
                elif 0< (self.fitness_value - herbivore.fitness_value) < self.parameters['deltaPhiMax']:
                    p_eating =  (self.fitness_value - herbivore.fitness_value)/self.parameters['deltaPhiMax']
                else:
                    p_eating = 1

                if p_eating > random.random():
                    herbivore.death = True
                    if(herbivore.weight <= appetite):
                        self.weight += herbivore.weight * self.parameters['beta']
                        self.fitness()
                        appetite -= herbivore.weight
                    else:
                        self.weight += appetite * self.parameters['beta']
                        self.fitness()
                        break
                else:
                    continue





def set_animal_params(species, params):
    """

    Parameters
    ----------
    species : str
        Class of animal, *'Herbivore'* or *'Carnovire'*

    params : dict
        Dictionary of *parameters* for each type of animal.

        .. seealso::
            - Animals.update_defaults()
    |

    """
    if species == 'Herbivore':
        Herbivores.set_params(params)
    elif species == 'Carnivore':
        Carnivores.set_params(params)
    else:
        raise ValueError('Cannot identify species')










