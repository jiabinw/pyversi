#!/usr/bin/env python
import os, sys
from tabuleiro import *
import pygame
from pygame.locals import *
from pgu import gui

class Game:
    tab = ''
    estadoJogo = 0	#0 = nao iniciado; 1 = jogo iniciado, 1 jogador; 2 = jogo iniciado, 2 jogadores
    inicializado = 0
    
    def input(self,events):
	if self.estadoJogo == 0:
	   for event in events: 
                if event.type == QUIT: 
                    sys.exit(0)
                else:
                    self.app.event(event) 
	
	elif self.estadoJogo == 1 or self.estadoJogo == 2:
           for event in events: 
                if event.type == QUIT: 
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    self.tab.click(event.dict['pos'][0],event.dict['pos'][1])
                    self.app.event(event)
                else:
                    self.app.event(event)

    def umJogadorEventHandler(self, event):
	self.estadoJogo = 1
	self.inicializado = 0

    def doisJogadoresEventHandler(self, event):
	self.estadoJogo = 2
	self.inicializado = 0
    
    def novoJogoEventHandler(self, event):
	self.estadoJogo = 0
	self.inicializado = 0
	
    def __init__(self):
        pygame.init()
        window = pygame.display.set_mode((329, 389), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('Reversi')
	while True:
	    self.inicializa()
	    self.inicializado = 1
	    while self.inicializado:
		window.fill((255,255,255))
		self.loop()

    def inicializa(self):
	if self.estadoJogo == 0:
		formf=gui.Form()
		self.app = gui.App()
		form = gui.Table()
		form.tr()
	
		e = gui.Button("1 jogador")
		e.connect(gui.CLICK, self.umJogadorEventHandler, None)
		form.td(e)
		b = gui.Button("2 jogadores")
		b.connect(gui.CLICK, self.doisJogadoresEventHandler, None)
		form.tr()
		form.td(b)
		c = gui.Container(align=-1,valign=-1)
		c.add(form,130,150)
		self.app.init(c)
	
	elif self.estadoJogo == 1 or self.estadoJogo == 2:
		formf=gui.Form()
		self.app = gui.App()
		form = gui.Table()
		form.tr()
		e = gui.Button("Novo Jogo")
		e.connect(gui.CLICK, self.novoJogoEventHandler, None)
		form.td(e)
	  
		c = gui.Container(align=-1,valign=-1)
		c.add(form,0,0)
	
		self.app.init(c)
		self.tab = Tabuleiro(pygame) 

    def loop(self):
	if self.estadoJogo == 0:
	    self.app.paint()
	    pygame.display.flip()
    	    self.input(pygame.event.get())


        elif self.estadoJogo == 1 or self.estadoJogo == 2:
	    self.tab.refresh()
	    self.app.paint()
	    pygame.display.flip()
	    self.input(pygame.event.get())


game = Game()

