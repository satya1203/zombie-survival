import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Zombie(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = ZOMBIE
        self.color = GREEN
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection