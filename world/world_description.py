"""
Just wold simulation

"""

from creatures import Plant, Herbivore
import random
import numpy as np


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

    # def __str__(self):
    #     return ' '.join([str(len(self.herbivores)),
    #                      str(len(self.predators)),
    #                      str(self.plant)])


class World:
    def __init__(self, shape: tuple):
        self.shape = shape
        self.field = self.create_field()

    def create_field(self):
        field = np.asarray([[Node() for i in range(self.shape[0])]
                            for j in range(self.shape[1])])

        return field

    def fill_field(self):
        for row in self.field:
            for el in row:
                if random.randint(0, 1):
                    el.add_plant(Plant())
                if random.randint(0, 5) == 0:
                    el.add_herbivore(Herbivore(sex=random.randint(0, 1)))

    def choose_borders(self, i, j):

        if i == 0:
            i_prev = 0
        else:
            i_prev = i - 1

        if i == len(self.field) - 1:
            i_next = len(self.field)
        else:
            i_next = i + 2

        if j == 0:
            j_prev = 0
        else:
            j_prev = j - 1

        if j == len(self.field[0]) - 1:
            j_next = len(self.field)
        else:
            j_next = j + 2

        return i_next, i_prev, j_next, j_prev

    def make_step(self):
        herbivores_stepped = list()

        for i, row in enumerate(self.field):
            for j, el in enumerate(row):

                i_next, i_prev, j_next, j_prev = self.choose_borders(i, j)
                field_part = self.field[i_prev: i_next, j_prev: j_next]

                for herbivore in el.herbivores:
                    if herbivore not in herbivores_stepped:
                        if el.plant:
                            if el.plant.hp > 0:
                                herbivore.eat(el.plant)
                            else:
                                el.remove_plant(el.plant)

                        herbivore.move(el, field_part)
                        herbivores_stepped.append(herbivore)

                if el.plant:
                    if el.plant.hp < 60:

                        x = np.random.randint(0, len(field_part) - 1)
                        y = np.random.randint(0, len(field_part[0]) - 1)

                        field_part[x][y].plant = el.plant.reproduce()

    def show(self):
        for row in self.field:
            pr = ' '

            for el in row:
                if el.plant:
                    pr += '*' + str(len(el.herbivores)) + ' '
                else:
                    pr += '-' + str(len(el.herbivores)) + ' '

            print(pr)


world = World((4, 4))
world.fill_field()

for i in range(3000):
    world.make_step()
    world.show()
    print('_' * 15)
