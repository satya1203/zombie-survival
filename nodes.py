import pygame
from vector import Vector2
from constants import *
import numpy as np

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}

    # tampilkan node di screen
    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

class NodeGroup(object):
    # bikin node
    def __init__(self, level):
        # map dari text file
        self.level = level 
        # Look Up Table : dictionary untuk node
        self.nodesLUT  = {}
        self.nodeSymbols = ['+']
        self.pathSymbols = ['.']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

    # baca file text, dtype supaya tidak dibaca sebagai float
    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    # membuat table node
    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                # setiap ada char '+' masukkan node ke LUT
                if data[row][col] in self.nodeSymbols:
                    # convert row & column ke nilai pixel
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    # menghubungkan node secara horizontal
    # jika menemukan node yang keynya tidak None, maka pasti node tsb terhubung horizontal
    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                # mencari char '+'
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        # key = row + column sebuah node
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.constructKey(col + xoffset, row + yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                # jika bukan char '.' berarti key = none
                elif data[row][col] not in self.pathSymbols:
                    key = None

    # menghubungkan node secara vertikal
    def connectVertically(self, data, xoffset=0, yoffset=0):
        # tukar row & col
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                # mencari char '+'
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.constructKey(col + xoffset, row + yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                # jika bukan char '.' berarti key = none
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    # ambil node dari nilai x & y tertentu
    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    # ambil node dari nilai col & row tertentu
    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    # player start node (temp)
    def getStartTempNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)
    
    # portal berpindah pada 2 titik dengan 2 arah
    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

