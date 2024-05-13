"""
This module implements the Landscape class representing a single square on the island.
There are four subclasses in this module which represent the four types of cells on the island that are
Water, Desert, Highland, and Lowland.

"""

import itertools
import math
import random
from biosim.animal import Herbivores
from biosim.animal import Carnivores
from biosim.animal import set_animal_params


class Landscape:
    """
       The Landscape class.

       Attributes
       ----------
       loc
           Tuple indicating location of cell on the island, starts at (1,1).
       h_pop
           List of herbivores present in the cell.
       h_pop_migrated
           List of migrated herbivores present in the cell.
       c_pop
           List of carnivores present in the cell.
       h_pop_migrated
           List of migrated carnivores present in the cell.
       fodder
           Amount of food available in the cell.
           |
       """
    f_max = None

    def __init__(self, loc):
        self.fodder = self.f_max
        self.loc = loc
        self.h_pop = []
        self.h_pop_migrated = []
        self.c_pop = []
        self.c_pop_migrated = []

    def get_num_h(self):
        return len(self.h_pop)

    def get_num_c(self):
        return len(self.c_pop)

    def add_animals(self, animals):
        """
        Add animals to their corresponding list (h_pop or c_pop) in Landscape class.

        Parameters
        ----------
        animals : list
            list of dictionaries that specify the species, age, and weight of each animal.

                """

        try:
            for x in animals:
                if x['species'] not in ['Herbivore', 'Carnivore']:
                    raise KeyError('Invalid species')
                elif x['species'] == 'Herbivore':
                    obj = Herbivores(x['age'], x['weight'])
                    self.h_pop.append(obj)
                elif x['species'] == 'Carnivore':
                    obj = Carnivores(x['age'], x['weight'])
                    self.c_pop.append(obj)

                # elif x['species'] == 'Carnivore':
                # obj = Carnivore(x['age'], x['weight'])
                # self.carnivores.append(obj)

        except RuntimeError as err:
            raise RuntimeError('ERROR: Failed while adding animal to Land: {}'.format(err))

    def aging(self):
        #print("Herbivore Age:")
        for herb in self.h_pop:
            herb.aging()
            #print(age)

        #print("Carnivore Age:")
        for carnivore in self.c_pop:
            carnivore.aging()
            #print(age)

    def death(self):
        def survivors(pop):
            return [herb for herb in pop if not herb.dies()]

        self.h_pop = survivors(self.h_pop)

        def survivors_carnivores(pop):
            return [carnivore for carnivore in pop if not carnivore.dies()]

        self.c_pop = survivors_carnivores(self.c_pop)

    def procreation(self):
        child_list_herb = []
        child_list_cornivore = []

        if len(self.h_pop) > 1:
            for herb in self.h_pop:
                if 0 < herb.weight > herb.update_min_weight():
                    child = herb.birth(len(self.h_pop) - 1)
                    if child is not None:
                        child_list_herb.append(child)

        self.h_pop = self.h_pop + child_list_herb

        if len(self.c_pop) > 1:
            for carnivore in self.c_pop:
                if 0 < carnivore.weight > carnivore.update_min_weight():
                    child = carnivore.birth(len(self.c_pop) - 1)
                    if child is not None:
                        child_list_cornivore.append(child)

        self.c_pop = self.c_pop + child_list_cornivore

    def feeding(self):
        """
        Animals feeding in a landcape
        """
        random.shuffle(self.h_pop)
        for herb in self.h_pop:
            self.fodder = herb.food(self.fodder)
        # print(self.fodder)

        #sorted in descending order when reverse in true
        self.c_pop.sort(key=lambda x: x.fitness_value, reverse=True)
        h_pop_merged = self.h_pop + self.h_pop_migrated
        h_pop_merged.sort(key=lambda x: x.fitness_value, reverse=False)
        for carnvore in self.c_pop:
            carnvore.feeds(h_pop_merged)
            self.h_pop = [herb for herb in self.h_pop if not herb.death]
            self.h_pop_migrated = [herb for herb in self.h_pop_migrated if not herb.death]
        # print("h_pop after carnivore eats")
        # print(self.h_pop)
        # print(self.h_pop_migrated)

    def loss_of_weight(self):
        """
            Animals loss_of_weight in a landcape
            Every year the animal losses some weight
        """
        for herb in itertools.chain(self.h_pop):
            herb_weight_loss = herb.loss_of_weight()
            # print(herb_weight_loss)

        for carnivore in itertools.chain(self.c_pop):
            carn_loss_weight = carnivore.loss_of_weight()
            # print(carn_loss_weight)

    def refill_food(self):
        """
        The amount of food is reseted every year in a landscape
        """
        self.fodder = self.f_max

    def combine_animal_list(self):
        # print("Herbivore:", len(self.h_pop), len(self.h_pop_migrated))
        self.h_pop += self.h_pop_migrated
        self.h_pop_migrated.clear()
        # print("Herbivore:", len(self.h_pop), len(self.h_pop_migrated))
        # print("Carnivore:", len(self.c_pop), len(self.c_pop_migrated))
        self.c_pop += self.c_pop_migrated
        self.c_pop_migrated.clear()
        # print("Carnivore:", len(self.c_pop), len(self.c_pop_migrated))

    def migration(self):
        """
        Animals migrating from one cell to another
        """
        mig_candidate = []
        rand_loc = []
        for herb in self.h_pop:
            if not herb.migration_probability():
                possible_lands = self.adjacent_lands(self.loc)
                rand_loc.append(random.choice(possible_lands))
                mig_candidate.append(herb)
        for carns in self.c_pop:
            if not carns.migration_probability():
                possible_lands = self.adjacent_lands(self.loc)
                rand_loc.append(random.choice(possible_lands))
                mig_candidate.append(carns)

        return mig_candidate, rand_loc

    def move_animal(self, animal):
        """
        When animal migrates, it needs to removed from the h_pop and c_pop of that cell
        """
        if animal in self.h_pop:
            self.h_pop.remove(animal)
            animal.migrated = True
            #print("Herbivore Remaining:", self.h_pop)
        else:
            self.c_pop.remove(animal)
            #print("Carnivore Remaining:", self.c_pop)

    def add_migrated_animal(self, animal):
        """
        List of migrated animals
        """
        if animal.__class__.__name__ == 'Herbivores':
            animal.aging()
            animal.loss_of_weight()
            if not animal.dies():
                self.h_pop_migrated.append(animal)
            # print("Migrated Animal:", self.h_pop_migrated)
        else:
            animal.aging()
            animal.loss_of_weight()
            if not animal.dies():
                self.c_pop_migrated.append(animal)
            # print("Migrated Animal:", self.c_pop_migrated)


    def adjacent_lands(self, loc):
        """
        List of adjacent lands from where the animal wants to migrate.
        """
        adjacent_land_list = [(loc[0] - 1, loc[1]), (loc[0] + 1, loc[1]), (loc[0], loc[1] - 1), (loc[0], loc[1] + 1)]
        return adjacent_land_list


class LowLand(Landscape):
    """
    'Lowland' Land type: allows animals to enter and has fodder.
    """

    f_max = 800
    allows_animal = True

    def __init__(self, loc):
        super().__init__(loc)


class HighLand(Landscape):
    """
    'Highland' Land type: allows animals to enter and has low fodder than the lowland
    """
    f_max = 300.0
    allows_animal = True

    def __init__(self, loc):
        super().__init__(loc)

class Desert(Landscape):
    """
    'Desert' Land type: allows animals to enter and has no fodder.
    """
    f_max = 0.0
    allows_animal = True

    def __init__(self, loc):
        super().__init__(loc)


class Water(Landscape):
    """
    'Water' Land type: animals cant enter.
    """
    f_max = 0.0
    allows_animal = False

    def __init__(self, loc):
        super().__init__(loc)


def update_animal_params(species, params):
    """
    Update animal parameters.

    |

    """
    set_animal_params(species, params)
