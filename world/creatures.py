"""
All world creatures

"""

import random


class Plant:
    def __init__(self, hp=100):
        self.hp = hp
        self.is_alive = True

    def subtract_hp(self, amount: int):
        if self.is_alive:
            self.hp -= amount

        if self.hp < 0:
            self.is_alive = False

    def reproduce(self):
        if self.is_alive:
            return Plant(self.hp)


class Herbivore:
    def __init__(self, sex):
        self.is_alive = True
        self.sex = sex

        self.hunger = 0
        self.age = 0

    def eat(self, plant: Plant):
        plant.subtract_hp(15)

        self.hunger -= 15

        if self.hunger < -100:
            self.hunger = -100

    def no_food(self):
        if self.hunger > 100:
            self.is_alive = False
        else:
            self.hunger += 25

    def reproduce(self, herbivore):
        if self.sex != herbivore.sex:

            sex = random.randint(0, 1)

            return Herbivore(sex)

    def move_from_to(self, herbivore, node1, node2):
        node2.add_herbivore(node1.remove_herbivore(herbivore))

    def move(self, node, field_part):
        res_scores = list()
        max_score_node = field_part[0:1, 0:1][0][0]
        max_score = self.get_cost(field_part[0:1, 0:1][0][0])
        # print(max_score_node)

        for row in field_part:

            row_scores = list()
            for el in row:

                score = self.get_cost(el)
                row_scores.append(score)

                if score > max_score:
                    max_score = score
                    max_score_node = el

            res_scores.append(row_scores)

        self.move_from_to(self, node, max_score_node)

    def get_cost(self, el):
        res = 0

        plant_bonus = 4
        herb_bonus = 3
        pred_fine = 4

        # print('Element', el)
        # for row in field_small:
        #     for el in row:
        if len(el.herbivores) < 2:
            res += len(el.herbivores) * herb_bonus
        else:
            res -= herb_bonus

        res -= len(el.predators) * pred_fine

        if el.plant is not None:
            res += plant_bonus * (el.plant.hp / 100)
        else:
            res -= plant_bonus

        return res


# field = [[Node() for i in range(3)] for j in range(3)]
#
# for row in field:
#     for el in row:
#         el.add_plant(Plant())
#         if random.randint(0, 1):
#             el.add_herbivore(Herbivore(sex=random.randint(0, 1)))
#
# for row in field:
#     pr = ' '
#
#     for el in row:
#         pr += str(len(el.herbivores)) + ' '
#
#     print(pr)
#
# for row in field:
#     for el in row:
#         if len(el.herbivores) != 0:
#             el.herbivores[0].move(el, field)
#
# for row in field:
#     pr = ' '
#
#     for el in row:
#         pr += str(len(el.herbivores)) + ' '
#
#     print(pr)
#
