#!/usr/bin/env python
import os, sys, copy
from peca import *
import time
from checkbox.message import Message

class Tabuleiro:
    pygame = 0
    ImgSurface = 0
    offset = (0,60)
    size = (341,341)
    tabuleiro = []
    IMGPATH = os.path.join("img","tabuleiro.png")
    pontosVermelho = 0
    pontosPreto = 0
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
        peca = Peca()
        ren = self.font.render(" Pontuacao",1,(0,0,0))
        screen.blit(ren,(120,0))

        #peca vermelha
        peca.estado = 1	
        pontVerm = self.font.render(":" + str(self.pontosVermelho),1,(255,0,0))
        screen.blit(pontVerm,(155,30))
        screen.blit(peca.img(), (120, 20))

        #peca preta
        peca.estado = 2
        pontPreto = self.font.render(":" + str(self.pontosPreto),1,(0,0,0))
        screen.blit(pontPreto,(220, 30))
        screen.blit(peca.img(), (185, 20))

        #cronometro
        cron = self.font.render(" Tempo",1,(0,0,0))
        screen.blit(cron,(250,0))
        clock = pygame.time.Clock()
        segundos = int(round(pygame.time.get_ticks()/1000))
        minutos = int(round(segundos/60))
        segundos = int(round(segundos % 60))
        
        cronometro = ('%02d:%02d' % (minutos, segundos))
        tempo = self.font.render(str(cronometro), 1, (0,0,0))
        screen.blit(tempo, (260, 30))


        for i in range(8):
            for j in range(8):
                item = self.tabuleiro[i][j]
                if item.estado != 0:
                    newsurface = item.img()
                    screen.blit(newsurface, (i*41 + 5 + self.offset[0], j*41 + 5 + self.offset[1]))
 
    def fimJogo(self):
        fim=1        
        for i in range(8):
            for j in range(8):
                item = self.tabuleiro[i][j]
                if item.estado == 0:
                    fim=0
                    break
        if fim == 1:
            print("fim")            
            return 1
        
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
        self.fimJogo()
        self.pontuacao()
        

    def pontuacao(self):
        self.pontosVermelho = 0
        self.pontosPreto = 0
        for i in range(8):
            for j in range(8):
                peca = self.tabuleiro[i][j]
                if peca.estado == 1:
                    self.pontosVermelho = self.pontosVermelho + 1
                elif peca.estado == 2:
                    self.pontosPreto = self.pontosPreto + 1

        
    def map(self, x, i):
        return int(round((x-self.offset[i])/41,0))
        
    def alternador(self):
        if self.last == 1:
            self.last = 2
        else:
            self.last = 1
        return self.last
