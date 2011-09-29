#!/usr/bin/env python
import os, sys
import pygame
from tabuleiro import *
from pygame.locals import *

class Game:
    
    def input(self,events): 
           for event in events: 
              if event.type == QUIT: 
                 sys.exit(0) 
              else:
                 print event
    
    def __init__(self):
        pygame.init()
        window = pygame.display.set_mode((329, 329))
        pygame.display.set_caption('Reversi')
        tab = Tabuleiro(pygame)
                 
    
        while True: 
           self.input(pygame.event.get())
           tab.refresh()

   
myGame = Game()
