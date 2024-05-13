import math
import random


class Herbivores:
    default_parameters = {'w_birth': 8,
                          'sigma_birth': 1.5,
                          'beta': 0.9,
                          'eta': 0.05,
                          'a_half': 40,
                          'phi_age': 0.2,
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
        self.age = age
        self.weight = weight
        self.offspring = False
        self.birth_count = 0
        # self.fodder = 800
        print("instance created")

    def aging(self):
        self.age += 1
        return self.age

    def fitness(self):
        phi_age = self.default_parameters['phi_age']
        age_half = self.default_parameters['a_half']
        phi_weight = self.default_parameters['phi_weight']
        weight_half = self.default_parameters['w_half']
        q_plus = 1 / (1 + math.exp(phi_age * (self.age - age_half)))
        q_minus = 1 / (1 + math.exp(-phi_weight * (self.weight - weight_half)))

        if self.weight <= 0:
            self.fitness_value = 0
        else:
            self.fitness_value = q_plus * q_minus

        return self.fitness_value

    def b_weight(self):
        mu = math.log((self.default_parameters['w_birth'] * self.default_parameters['w_birth']) / math.sqrt(
            (self.default_parameters['w_birth'] * self.default_parameters['w_birth']) + (
                        self.default_parameters['sigma_birth'] * self.default_parameters['sigma_birth'])))
        sigma = math.log(1 + (((self.default_parameters['sigma_birth']) * (self.default_parameters['sigma_birth'])) / (
                    (self.default_parameters['w_birth']) * (self.default_parameters['w_birth']))))

        self.birth_weight = random.lognormvariate(mu, sigma)
        return self.birth_weight

    def loss_of_weight(self):
        self.weight = self.weight - self.default_parameters['eta'] * self.weight
        return self.weight

    def food(self, fodder):
        if self.default_parameters['F'] < fodder:
            fodder = fodder - self.default_parameters['F']
            self.weight = self.weight + self.default_parameters['beta'] * self.default_parameters['F']
        else:
            self.weight = self.weight + self.default_parameters['beta'] * fodder
            fodder = 0
        print("Weight after eating:......", self.weight)
        return fodder

    def birth(self, N):
        min_weight = (self.default_parameters['zeta']) * (
                    self.default_parameters['w_birth'] + self.default_parameters['sigma_birth'])
        if (min_weight < self.weight):
            mu = math.log((self.default_parameters['w_birth'] * self.default_parameters['w_birth']) / math.sqrt(
                (self.default_parameters['w_birth'] * self.default_parameters['w_birth']) + (
                        self.default_parameters['sigma_birth'] * self.default_parameters['sigma_birth'])))
            sigma = math.log(1 + (
                        ((self.default_parameters['sigma_birth']) * (self.default_parameters['sigma_birth'])) / (
                            (self.default_parameters['w_birth']) * (self.default_parameters['w_birth']))))
            offspring_weight = random.lognormvariate(mu, sigma)
            weight_loss = self.default_parameters['zeta'] * offspring_weight
            if (weight_loss < self.weight):
                p_birth = min(1, self.default_parameters['gamma'] * self.fitness() * N)
                if (random.random() < p_birth):
                    self.birth_count = self.birth_count + 1
                    return type(self)(age=0, weight=offspring_weight)
                else:
                    return None
            else:
                return None
        else:
            return None

        # if not self.offspring:
        #     p_birth = min(1, self.default_parameters['gamma'] * self.fitness() * N)
        #     if self.weight >= ((self.default_parameters['zeta']) * (self.default_parameters['w_birth'] + self.default_parameters['sigma_birth'])) and (random.random() < p_birth):
        #         offspring_weight = self.b_weight()
        #         if self.weight < self.default_parameters['zeta'] * self.offspring_weight:
        #             self.offspring = False
        #         else:
        #             self.offspring = True
        #             self.weight = self.weight - self.default_parameters['zeta'] * self.offspring_weight
        #             return self.offspring
        #
        # return self.offspring

    def dies(self):
        death = False
        p_death = self.default_parameters['omega'] * (1 - self.fitness())
        if self.weight == 0 or random.random() < p_death:
            death = True
        return death
