"""
Just wold simulation

"""

from .creatures import Plant, Herbivore
import random


class Node:
    def __init__(self):
        self.max_els = 4
        self.num_els = 0

        self.herbivores = list()
        self.predators = list()
        self.plant = None

    def add_herbivore(self, herbivore):
        if self.num_els < self.max_els:
            self.herbivores.append(herbivore)
            self.num_els += 1

    def add_predator(self, predator):
        if self.num_els < self.max_els:
            self.predators.append(predator)
            self.num_els += 1

    def add_plant(self, plant):
        self.plant = plant
        self.num_els += 1

    def remove_herbivore(self, herbivore):
        if herbivore in self.herbivores:
            self.herbivores.remove(herbivore)
            self.num_els -= 1

        return herbivore

    def remove_predator(self, predator):
        if predator in self.predators:
            self.predators.remove(predator)
            self.num_els -= 1

        return predator

    def remove_plant(self, plant):
        if self.plant and self.plant == plant:
            self.plant = None
            self.num_els -= 1

        return plant


    def __str__(self):
        return (self.herbivores,
                self.predators,
                self.plant)


class World:
    def __init__(self, shape: tuple):
        self.shape = shape
        self.field = self.create_field()

    def create_field(self):
        field = [[Node() for i in range(self.shape[0])]
                 for j in range(self.shape[1])]

        return field

    def fill_field(self):
        for row in self.field:
            for el in row:
                el.add_plant(Plant())
                if random.randint(0, 1):
                    el.add_herbivore(Herbivore(sex=random.randint(0, 1)))

    def make_step(self):
        pass


