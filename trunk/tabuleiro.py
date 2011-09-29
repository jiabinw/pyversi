#!/usr/bin/env python
import os, sys

class Tabuleiro:
    pygame = 0
    tabuleiro = []
    
    def __init__(self, game):
        self.pygame = game
        screen = game.display.get_surface()
        tabuleiroImgPath = os.path.join("img","tabuleiro.png")
        tabuleiroSurface = game.image.load(tabuleiroImgPath)
        screen.blit(tabuleiroSurface, (0,0))
        game.display.flip()
        row = [0]*8
        
        for item in row:
            self.tabuleiro.append(row)
        
    def refresh(self):
        self.pygame.display.flip()
        
    