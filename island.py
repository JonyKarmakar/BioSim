from landscape import LowLand
from landscape import Water


class Island:
    def __init__(self, map, herb_animals, carn_animals=None):
        self.map_list = [i for i in map if i != '\n']
        self.herb_animal_list = herb_animals
        self.carn_animal_list = carn_animals
        self.land_list = []
        self.location = None

        # print(self.map_list)
        # print(type(map))

    def add_lands(self):
        # Adding lands to island.
        for item in self.map_list:
            # print(item)
            if item == "L":
                land = LowLand()
                self.land_list.append(land)
            elif item == "W":
                land = Water()
                self.land_list.append(land)
            else:
                print("Error")

        return self.land_list

    def add_animal(self, popu):
        # adding animals to lands.
        for item in popu:
            animal = item['pop']
            print(animal)
            self.location = item['loc'][0] * item['loc'][1]
            print(self.location)
            print(self.land_list)
            land = self.land_list[self.location]
            print(land)

            land.add_animals(animal)

        # return land.get_num_h()

    def cycle(self):
        """Update all landscapes by one cycle."""
        land = self.land_list[self.location]
        print("FOOD REMAINING:...................")
        print(land.feeding())
        print("PROCREATION:...................")
        land.procreation()
        print("NO. OF herbivore AFTER PROCREATION:...................")
        print(land.get_num_h())
        print("NO. OF carnivore AFTER PROCREATION:...................")
        print(land.get_num_c())

        print("AGE:...................")
        land.aging()
        print("Weight after losing some:.....")
        land.loss_of_weight()
        land.death()
        land.refill_food()
        print("Survived number of Animals:")
        return land.get_num_h(), land.get_num_c()
