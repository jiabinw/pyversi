#!/usr/bin/env python
import os, sys
import pygame

class Peca:
    imgPath = [os.path.join("img","pecavermelha.png"), os.path.join("img","pecapreta.png")]
    imgSurface = [pygame.image.load(imgPath[0]),pygame.image.load(imgPath[1])]
    estado = 0 #0 = vazio, 1 = jogador vermelho, 2 = jogador preto
    
    def __init__(self):
        self.estado = 0
  
    def img(self):
        if (self.estado != 0):
            return self.imgSurface[self.estado-1]
        else:
            return ""

    def __str__(self):
        return "Peca com estado " + str(self.estado)
    
    def __repr__(self):
        return "Peca com estado " + str(self.estado)
        
    def flip(self):
        if self.estado == 1:
            self.estado = 2 
        elif self.estado == 2:
            self.estado = 1    
