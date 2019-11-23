"""
Just wold simulation

"""

from creatures import Plant, Herbivore, Predator
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
        else:
            print('Cant input', self.num_els)

    def add_plant(self, plant):
        if not self.plant:
            self.num_els += 1
        self.plant = plant

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
    def __init__(self, shape: tuple,
                 predators_chance=0.1,
                 herbivore_chance=0.3,
                 plants_chance=0.5,
                 predators_birth_chance=0.1,
                 herbivores_birth_chance=0.1,
                 plants_reproduce_chance=0.1):
        self.shape = shape
        self.field = self.create_field()
        self.predators_num = 0
        self.herbivore_num = 0
        self.plants_num = 0

        self.predators_chance = predators_chance
        self.herbivore_chance = herbivore_chance
        self.plants_chance = plants_chance
        self.predators_birth_chance = predators_birth_chance
        self.herbivores_birth_chance = herbivores_birth_chance
        self.plants_reproduce_chance = plants_reproduce_chance

    def create_field(self):
        field = np.asarray([[Node() for i in range(self.shape[0])]
                            for j in range(self.shape[1])])

        return field

    def fill_field(self):
        for row in self.field:
            for el in row:
                if random.uniform(0, 1) < self.plants_chance:
                    el.add_plant(Plant())
                    self.plants_num += 1
                if random.uniform(0, 1) < self.herbivore_chance:
                    el.add_herbivore(Herbivore(sex=random.randint(0, 1)))
                    self.herbivore_num += 1
                if random.uniform(0, 1) < self.predators_chance:
                    el.add_predator(Predator(sex=random.randint(0, 1)))
                    self.predators_num += 1

    def find_nums(self):
        result_pred = 0
        result_herb = 0
        result_plants = 0

        for row in self.field:
            for el in row:
                result_pred += len(el.predators)
                result_herb += len(el.herbivores)

                if el.plant:
                    result_plants += 1

        return [result_pred, result_herb, result_plants]

    def choose_borders(self, i, j, w=1):

        if i - w + 1 == 0:
            i_prev = 0
        else:
            i_prev = i - w

        if i == len(self.field) - w:
            i_next = len(self.field)
        else:
            i_next = i + 1 + w

        if j - w + 1 == 0:
            j_prev = 0
        else:
            j_prev = j - w

        if j == len(self.field[0]) - w:
            j_next = len(self.field[0])
        else:
            j_next = j + 1 + w

        return i_next, i_prev, j_next, j_prev

    def are_hungry(self, unit1, unit2):
        hunger = False

        if unit1.hunger > 50 or unit2.hunger > 50:
            hunger = True

        return hunger

    # def can_reproduce(self, node):
    #     result = node.num_els < node.max_els and len(el.herbivores) == 2 and \
    #             el.herbivores[0].sex != el.herbivores[1].sex and \
    #             random.uniform(0, 1) < self.herbivores_birth_chance and \
    #             not self.are_hungry(el.herbivores[0], el.herbivores[1]):

    def make_step(self):
        herbivores_stepped = list()
        herbivores_reproduced = list()
        predators_stepped = list()
        predators_reproduced = list()

        for i, row in enumerate(self.field):
            for j, el in enumerate(row):

                i_next, i_prev, j_next, j_prev = self.choose_borders(i, j)
                field_part = self.field[i_prev: i_next, j_prev: j_next]

                for herbivore in el.herbivores:

                    if herbivore not in herbivores_stepped:
                        # print(el.num_els < el.max_els, el.herbivores)
                        if el.num_els < el.max_els and len(el.herbivores) == 2 and \
                                el.herbivores[0].sex != el.herbivores[1].sex and \
                                random.uniform(0, 1) < self.herbivores_birth_chance and \
                                not self.are_hungry(el.herbivores[0], el.herbivores[1]):

                            new_herbivore = el.herbivores[0].reproduce(el.herbivores[1])
                            herbivores_reproduced.append(el.herbivores[0])
                            herbivores_reproduced.append(el.herbivores[1])

                            el.add_herbivore(new_herbivore)
                            self.herbivore_num += 1

                        if herbivore.hunger > 50 and \
                                el.plant and el.plant.is_alive:
                            herbivore.eat(el.plant)

                            if not el.plant.is_alive:
                                el.remove_plant(el.plant)
                                self.plants_num -= 1
                        else:
                            herbivore.no_food()

                        if herbivore.is_alive:
                            herbivore.move(el, field_part)
                            herbivores_stepped.append(herbivore)
                        else:
                            el.remove_herbivore(herbivore)
                            self.herbivore_num -= 1

                i_next_p, i_prev_p, j_next_p, j_prev_p = self.choose_borders(i, j, w=3)
                field_part_p = self.field[i_prev_p: i_next_p, j_prev_p: j_next_p]

                for predator in el.predators:

                    if predator not in predators_stepped:
                        if el.num_els < el.max_els and len(el.predators) == 2 and \
                                el.predators[0].sex != el.predators[1].sex and \
                                random.uniform(0, 1) < self.predators_birth_chance and \
                                not self.are_hungry(el.predators[0], el.predators[1]):

                            new_predator = el.predators[0].reproduce(el.predators[1])
                            predators_reproduced.append(el.predators[0])
                            predators_reproduced.append(el.predators[1])

                            el.add_predator(new_predator)
                            self.predators_num += 1

                        if el.herbivores and predator.hunger > 30\
                                and random.choice((0, 1)) < 0.05:
                            herbivore = random.choice(el.herbivores)
                            predator.eat(herbivore)
                            el.remove_herbivore(herbivore)
                            self.herbivore_num -= 1
                        else:
                            predator.no_food()

                        if predator.is_alive:
                            predator.move(el, field_part_p)
                            herbivores_stepped.append(predator)
                        else:
                            el.remove_predator(predator)
                            self.predators_num -= 1

                if el.plant:
                    if el.plant.hp < 40 and\
                            el.plant.is_alive and \
                            random.uniform(0, 1) < self.plants_reproduce_chance:

                        x = np.random.randint(0, len(field_part) - 1)
                        y = np.random.randint(0, len(field_part[0]) - 1)

                        if not field_part[x][y].plant:
                            self.plants_num += 1

                        field_part[x][y].plant = el.plant.reproduce()

    def logs(self):
        return (
            ('Plants number', self.plants_num),
            ('Herbivore number', self.herbivore_num),
            ('Predators number', self.predators_num)
        )

    def show(self):
        for row in self.field:
            pr = ' '

            for el in row:
                if el.plant:
                    pr += '*(' + str(len(el.herbivores)) + 'h)(' + str(len(el.predators)) + 'p) '
                else:
                    pr += '-(' + str(len(el.herbivores)) + 'h)(' + str(len(el.predators)) + 'p) '

            print(pr)
