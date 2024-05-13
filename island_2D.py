import random

import numpy as np

from landscape import LowLand
from landscape import HighLand
from landscape import Desert
from landscape import Water
import landscape
import textwrap


class Island2d:
    def __init__(self, maps, herb_animals, carn_animals):
        self.map_list = [i for i in maps.split()]
        self.herb_animal_list = herb_animals
        self.carn_animal_list = carn_animals
        self.land_list = []
        self.location = None
        # print(self.map_list)
        # print(type(map))

    def map_validate(self):
        boundary = False
        map_list_t = []
        bound1 = ''
        bound2 = ''
        for i in self.map_list:
            bound1 += i[0]
            bound2 += i[-1]
        map_list_t.append(bound1)
        map_list_t.append(bound2)
        # print(map_list_t)

        if self.map_list[0] == 'W' * len(self.map_list[0]) and self.map_list[-1] == 'W' * len(self.map_list[-1]) and \
                map_list_t[0] == 'W' * len(map_list_t[0]) and map_list_t[0] == 'W' * len(map_list_t[1]):
            boundary = True
        else:
            boundary = False

        return boundary

    def add_lands(self):
        row = 0
        # Adding lands to island.
        if self.map_validate():
            for item in self.map_list:
                row_list = []
                column = 0
                for cell in item:
                    loc = row, column
                    if cell == "L":
                        land = LowLand(loc)
                        row_list.append(land)
                    elif cell == "W":
                        land = Water(loc)
                        row_list.append(land)
                    elif cell == "D":
                        land = Desert(loc)
                        row_list.append(land)
                    elif cell == "H":
                        land = HighLand(loc)
                        row_list.append(land)
                    else:
                        print("Error")
                    column += 1
                self.land_list.append(row_list)
                row += 1

            return self.land_list
        else:
            raise ValueError("Boundary is not okay!")

    def add_animal(self, popu):
        # adding animals to lands.
        for item in popu:
            animal = item['pop']
            # print(animal)
            self.location = item['loc']
            # print(self.location[0])
            # print(self.land_list)
            land = self.land_list[self.location[0] - 1][self.location[1] - 1]
            # print("Check Location:")
            # print(land)

            land.add_animals(animal)

    def migrate(self, land):
        # for land in self.land_list:
        #     for cell in land:
        #         print("Current Land", cell)
        #         print(cell.get_num_h())
        #         loc = (self.land_list.index(land), land.index(cell))
        #         if cell.allows_animal and cell.migration:
        #             possible_lands = cell.adjacent_lands(loc)
        #             rand_loc = random.choice(possible_lands)
        #             print("Chosen Land", self.land_list[rand_loc[0]][rand_loc[1]])
        #             if self.land_list[rand_loc[0]][rand_loc[1]].allows_animal:
        #                 print("Migration Possible!")
        #                 moved_animal = cell.move_animal()
        #                 self.land_list[rand_loc[0]][rand_loc[1]].add_migrated_animal(moved_animal)
        ######Check######
        # for land in self.land_list:
        #     for cell in land:
        #         print("Current Land", cell)
        #         print(cell.get_num_h())
        #         # loc = (self.land_list.index(land), land.index(cell))

        cells = land

        if cells.allows_animal:
            rand_loc_and_animal = cells.migration()
            # self.land_list[rand_loc[0]][rand_loc[1]].add_migrated_animal(moved_animal)
            #print(rand_loc_and_animal)
            rand_loc = rand_loc_and_animal[1]
            mig_candidate = rand_loc_and_animal[0]
            i = 0
            for item in rand_loc:
                if self.land_list[item[0]][item[1]].allows_animal:
                    cells.move_animal(mig_candidate[i])
                    self.land_list[item[0]][item[1]].add_migrated_animal(mig_candidate[i])
                    # print(mig_candidate[i])
                i += 1

    def animal_count(self):
        for land in self.land_list:
            for cell in land:
                print('Location: ', cell.loc)
                print('Herbivores:', cell.get_num_h())

    def cycle(self):
        """Update all landscapes by one cycle."""
        # land = self.land_list[self.location]
        total_h = 0
        total_c = 0
        for land_row in self.land_list:
            for land in land_row:
                if land.__class__.__name__ == 'Water':
                    pass
                else:
                    # total_animal = land.get_num_h() + land.get_num_c()
                    # if total_animal == 0:
                    #     pass
                    # else:
                    # print("PROCREATION:...................")
                    land.feeding()
                    land.procreation()
                    # print("FOOD REMAINING:...................")
                    # print(land.feeding())
                    # print("NO. OF herbivore AFTER PROCREATION:...................")
                    # print(land.get_num_h())
                    # print("NO. OF carnivore AFTER PROCREATION:...................")
                    # print(land.get_num_c())
                    self.migrate(land)
                    # print("AGE:...................")
                    land.aging()
                    # print("Weight after losing some:.....")
                    land.loss_of_weight()
                    land.death()
                    land.refill_food()
                    land.combine_animal_list()
                    # print("Survived number of Animals:")
                    total_h += land.get_num_h()
                    total_c += land.get_num_c()

        return total_h, total_c

# geogr = """\
#            WWWWW
#            WLDLW
#            WDHLW
#            WDDDW
#            WWWWW"""
#
# # geogr = """\
# #            WWWWWWWWWWWWWWWWWWWWW
# #            WHHHHHLLLLWWLLLLLLLWW
# #            WHHHHHLLLLWWLLLLLLLWW
# #            WHHHHHLLLLWWLLLLLLLWW
# #            WWHHLLLLLLLWWLLLLLLLW
# #            WWHHLLLLLLLWWLLLLLLLW
# #            WWWWWWWWHWWWWLLLLLLLW
# #            WHHHHHLLLLWWLLLLLLLWW
# #            WHHHHHHHHHWWLLLLLLWWW
# #            WHHHHHDDDDDLLLLLLLWWW
# #            WHHHHHDDDDDLLLLLLLWWW
# #            WHHHHHDDDDDLLLLLLLWWW
# #            WHHHHHDDDDDWWLLLLLWWW
# #            WHHHHDDDDDDLLLLWWWWWW
# #            WWHHHHDDDDDDLWWWWWWWW
# #            WWHHHHDDDDDLLLWWWWWWW
# #            WHHHHHDDDDDLLLLLLLWWW
# #            WHHHHDDDDDDLLLLWWWWWW
# #            WWHHHHDDDDDLLLWWWWWWW
# #            WWWHHHHLLLLLLLWWWWWWW
# #            WWWHHHHHHWWWWWWWWWWWW
# #            WWWWWWWWWWWWWWWWWWWWW"""
# geogr = textwrap.dedent(geogr)
#
# ini_herbs = [{'loc': (2, 4),
#               'pop': [{'species': 'Herbivore',
#                        'age': 5,
#                        'weight': 20}
#                       for _ in range(3)]}]
#
# ini_herbs2 = [{'loc': (3, 4),
#               'pop': [{'species': 'Herbivore',
#                        'age': 5,
#                        'weight': 20}
#                       for _ in range(3)]}]
#
# obj = Island2d(geogr, ini_herbs)
# # print(obj.add_lands())
# obj.add_lands()
# obj.add_animal(ini_herbs)
# obj.add_animal(ini_herbs2)
#
# obj.migrate()
# obj.animal_count()
#
# # print("Animal cannot be in water!")
#
# # print(obj.add_lands())
# # i=2
# # j=4
# # print(obj.land_list[i-1][j-1])
