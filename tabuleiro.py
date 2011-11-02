#!/usr/bin/env python
import os, sys, copy
from peca import *

class Tabuleiro:
    pygame = 0
    ImgSurface = 0
    offset = (0,30)
    size = (341,341)
    tabuleiro = []
    IMGPATH = os.path.join("img","tabuleiro.png")

    last = 2
    
    def __init__(self, game):
        self.font = pygame.font.SysFont("Courier New", 18)
        self.pygame = game       
        self.ImgSurface = self.pygame.image.load(self.IMGPATH)
        row = [0]*8
        
        for item in row:
            self.tabuleiro.append(copy.deepcopy(row))
            
        self.initPecas()
        
    def refresh(self):
        screen = self.pygame.display.get_surface()        
        screen.blit(self.ImgSurface, self.offset)
        
        #escreve a pontuacao na tela        
        ren = self.font.render("teste",1,(255,255,255))
        screen.blit(ren,(120,0))
        
        for i in range(8):
            for j in range(8):
                item = self.tabuleiro[i][j]
                if item.estado != 0:
                    newsurface = item.img()
                    screen.blit(newsurface, (i*41 + 5 + self.offset[0], j*41 + 5 + self.offset[1]))
        self.pygame.display.flip()        
        
    def initPecas(self):
        for i in range(8):
            for j in range (8):
                self.tabuleiro[i][j] = Peca()
    
    def click(self, x, y):
        if x < self.offset[0] or x > self.size[0] + self.offset[0]:
            return
        if y < self.offset[1] or y > self.size[1] + self.offset[1]:
            return
	
        peca = self.tabuleiro[self.map(x, 0)][self.map(y, 1)]
        if peca.estado == 0:
            peca.estado = self.alternador()
        else:
            peca.estado = peca.estado

        
    def map(self, x, i):
        return int(round((x-self.offset[i])/41,0))
        
    def alternador(self):
        if self.last == 1:
            self.last = 2
        else:
            self.last = 1
        return self.last
