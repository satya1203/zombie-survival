import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class Zombie(Entity):
    def __init__(self, node, player=None):
        Entity.__init__(self, node)
        self.name = ZOMBIE
        self.color = GREEN
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.player = player
        self.mode = ModeController(self)

        
    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is WANDER:
            self.wander()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def wander(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.player.position

    # reset zombie saat player mati
    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection