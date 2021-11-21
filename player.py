import pygame
from pygame.locals import *
from vector import Vector2
from constants import *

class Player(object):
    def __init__(self, node):
        self.name = PLAYER
        self.directions = {
            UP:Vector2(0, -1), 
            DOWN:Vector2(0, 1), 
            LEFT:Vector2(-1, 0), 
            RIGHT:Vector2(1, 0), 
            STOP:Vector2()
        }
        # arah awal
        self.direction = STOP
        self.speed = 100
        # besar player
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.setPosition()
        # target (player pergi ke mana)
        self.target = node

    # salin posisi vector
    def setPosition(self):
        self.position = self.node.position.copy()

    # cek keyboard input
    def update(self, dt):
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.direction = STOP
            self.setPosition()

    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    # draw player
    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

    # cek jika player overshot target node
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            # jika jarak player lebih dari jarak 2 node return true
            return node2Self >= node2Target
        return False

    # ganti arah
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    # cek input keyboard kebalikan dari arah
    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False