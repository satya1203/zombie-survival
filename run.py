import pygame
from pygame.locals import *
from constants import *
from player import Player
from nodes import NodeGroup
from zombies import Zombie

class GameController(object):
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

    # create background
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("maze1.txt")
        # set koordinat titik portal
        self.nodes.setPortalPair((0,17), (27,17))
        self.player = Player(self.nodes.getStartTempNode())
        self.zombie = Zombie(self.nodes.getStartTempNode(), self.player)

    # dipanggil tiap ganti frame (gameloop)
    def update(self):
        # waktu dalam detik
        dt = self.clock.tick(30) / 1000.0
        self.player.update(dt)
        self.zombie.update(dt)
        # cek event tertentu
        self.checkEvents()
        # draw image ke screen
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        # gambar ulang supaya tidak tumpang tindih
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.player.render(self.screen)
        self.zombie.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
