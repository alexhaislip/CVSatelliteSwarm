from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import pygame
from pygame.locals import *
from collections import namedtuple
import random
from vec2d import Vec2d
import math

Coordinate = Vec2d

class Robot():
    MAX_SPEED = 0.1
    MAX_ROT_SPEED = 0.1

    def __init__(self):
        self.position = Vec2d((0,0))
        self.direction = 0

        self.target = None

        #DEBUG:
        self.mean_direction = Vec2d((0,0))

        self.avoid_radius = 50

    def set_target(self, coords):
        if coords == None:
            self.target = None
            return

        self.target = Vec2d(coords)
        self.direction = (self.target - self.position).normalized()

    def tick(self, time, global_robots):

        movement = Vec2d(0,0)

        if self.target is not None:
            if self.position.get_distance(self.target) < 10:
                self.seek_target = False
                self.avoid_radius = 20
                self.direction = Vec2d((0,0))
            else:
                self.seek_target = True
                self.avoid_radius = 50
                self.direction = (self.target - self.position).normalized()

        robots = filter(lambda x: id(x) != id(self), global_robots)

        near_robots = filter(lambda x: self.position.get_distance(x.position) < min(
            self.avoid_radius, x.avoid_radius), robots)

        near_robots = [self.position - x.position for x in near_robots]

        if len(near_robots) > 0:
            #Average position of near_robots
            weighted_direction = map(lambda x: self.position.get_distance(x) * x * 0.0001,
                    near_robots)

            mean_direction = reduce(Vec2d.mean, weighted_direction)

            # DEBUG:
            self.mean_direction = mean_direction

            if mean_direction is not None:
                movement += mean_direction

        else:
            self.mean_direction = Vec2d(0,0)

        movement += self.direction
        self.position += time * movement * 0.1

    def draw(self, surface):
        xpos = int(self.position.x - 0)
        ypos = int(self.position.y - 0)

        pygame.draw.circle(surface, (0, 0, 0), (xpos,ypos), 10, 0)
        pygame.draw.circle(surface, (0, 0, 0), (xpos,ypos), self.avoid_radius, 2)
        pygame.draw.aaline(surface, (0,0,255), self.position, self.position+(self.direction*30), 10)
        pygame.draw.aaline(surface, (0,255,0), self.position, self.position-(self.mean_direction*30), 10)

        if self.target is not None:
            pygame.draw.circle(surface, (255,0,0), (xpos,ypos), 5, 0)

class App:
    def __init__(self):
        self._running = False
        self._display_surf = None
        self.size = self.width, self.height = 800, 600
        self._clock = pygame.time.Clock()

        self.robots = []

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                rob = Robot()
                rob.position = Coordinate(*pygame.mouse.get_pos())

                mag = 2

                self.robots.append(rob)

            if event.button == 3:
                for i in self.robots:
                    i.set_target((random.randint(0,800), random.randint(0,600)))

    def on_loop(self, time):
        """main loop"""
        for robot in self.robots:
            robot.tick(time, self.robots)

    def on_render(self, fps):
        """render surface"""
        self._display_surf.fill((255,255,255))

        for robot in self.robots:
            robot.draw(self._display_surf)

        pygame.display.set_caption("simulation - %02d fps" % fps)
        pygame.display.update()

    def on_cleanup(self):
        """cleanup"""

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop(self._clock.get_time())
            self.on_render(self._clock.get_fps())
            self._clock.tick(120)
        self.on_cleanup()

if __name__ == "__main__":
    app = App()
    app.on_execute()
