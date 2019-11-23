import random
from datetime import datetime, timedelta

import os
import time
import pygame
from pygame.rect import Rect

import config as c
from brick import Brick
from game import Game
from world_description import World

import colors


class Breakout(Game):
    def __init__(self, world: World):
        Game.__init__(self, 'Breakout', c.screen_width, c.screen_height, c.frame_rate)
        self.start_level = False
        self.dots = None
        self.is_game_running = False

        self.world = world
        self.world.fill_field()

        self.draw_field()

    def draw_field(self):
        bricks = []

        for j, row in enumerate(self.world.field):

            for i, el in enumerate(row):
                brick_color = colors.YELLOW1

                if el.predators:
                    brick_color = colors.INDIANRED
                elif el.herbivores:
                    brick_color = colors.LIGHTBLUE
                elif el.plant:
                    brick_color = colors.GREEN

                w = c.brick_width
                h = c.brick_height

                brick = Brick(i * (w + 1),
                              j * (h + 1),
                              w,
                              h,
                              brick_color,
                              None)
                bricks.append(brick)
                self.objects.append(brick)

        self.dots = bricks

    def update(self):

        if self.game_over:
            self.show_message('GAME OVER!', centralized=True)

    def run(self):
        while not self.game_over:

            self.handle_events()
            self.update()
            self.draw()

            self.world.make_step()
            print(self.world.logs())

            self.objects = []
            self.draw_field()

            pygame.display.update()
            self.clock.tick(self.frame_rate)


def main():
    Breakout(World((70, 70),
                   predators_chance=0.125,
                   herbivore_chance=0.60,
                   plants_chance=0.3,
                   predators_birth_chance=0.1,
                   herbivores_birth_chance=0.2,
                   plants_reproduce_chance=0.50)).run()

# predators_chance=0.10,
# herbivore_chance=0.60,\
#                  plants_chance=0.3,
#                    predators_birth_chance=0.1,
#                    herbivores_birth_chance=0.2,
#                    plants_reproduce_chance=0.50

if __name__ == '__main__':
    main()
