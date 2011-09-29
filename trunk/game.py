#!/usr/bin/env python
import os, sys
from tabuleiro import *
import pygame
from pygame.locals import *
from pgu import gui

class Game:
    tab = ''
    
    def input(self,events): 
           for event in events: 
                if event.type == QUIT: 
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    self.tab.click(event.dict['pos'][0],event.dict['pos'][1])
                else:
                    self.app.event(event)
    
    def __init__(self):
        pygame.init()
        window = pygame.display.set_mode((329, 359),SWSURFACE)
        pygame.display.set_caption('Reversi')
        
        formf=gui.Form()
        self.app = gui.App()
        form = gui.Table()
        form.tr()
        e = gui.Button("Novo Jogo")
        form.td(e)
        
        c = gui.Container(align=-1,valign=-1)
        c.add(form,0,0)
        
        self.app.init(c)
        self.tab = Tabuleiro(pygame)      
    
        while True:
            self.app.paint()
            pygame.display.flip()
            self.input(pygame.event.get())
            self.tab.refresh()

game = Game()

