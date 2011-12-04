#!/usr/bin/env python
import os, sys
from tabuleiro import *
import pygame
from pygame.locals import *
from pgu import gui

class Game:
    tab = ''
    estadoJogo = 0	#0 = nao iniciado; 1 = jogo iniciado, 1 jogador jogando contra 1 heuristicas master; 2 = jogo iniciado, 2 jogadores; 3 = jogo entre comb.heuristicas
    inicializado = 0
    
    def input(self,events):
        if self.estadoJogo == 0:
           for event in events: 
                if event.type == QUIT: 
                    sys.exit(0)
                else:
                    self.app.event(event) 
        
        elif self.estadoJogo == 1:
           for event in events: 
                if event.type == QUIT: 
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.dict['pos'][0] > 120 and event.dict['pos'][0] < 185 and event.dict['pos'][1] > 270 and event.dict['pos'][1] < 335:
                        print "1jogador com a heuristica1=", self.heuristica1.value
                    self.app.event(event)
                else:
                    self.app.event(event)
        
        elif self.estadoJogo == 2:
           for event in events: 
                if event.type == QUIT: 
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    self.botaoHabilitado = self.tab.click(event.dict['pos'][0],event.dict['pos'][1])
                    self.app.event(event)
                else:
                    self.app.event(event)

        elif self.estadoJogo == 3:
           for event in events: 
                if event.type == QUIT: 
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.dict['pos'][0] > 120 and event.dict['pos'][0] < 185 and event.dict['pos'][1] > 270 and event.dict['pos'][1] < 335:
                        print "versus com a heuristica1=", self.heuristica1.value, " e heuristica2=", self.heuristica2.value 
                    self.app.event(event)
                else:
                    self.app.event(event)

    def umJogadorEventHandler(self, event):
        self.estadoJogo = 1
        self.inicializado = 0

    def doisJogadoresEventHandler(self, event):
        self.estadoJogo = 2
        self.inicializado = 0
        
    def zeroJogadoresEventHandler(self, event):
        self.estadoJogo = 3
        self.inicializado = 0
    
    def novoJogoEventHandler(self, event):
        self.estadoJogo = 0
        self.inicializado = 0
    
    def passarVezEventHandler(self, event):
        self.tab.alternador()

        
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
			e = gui.Label("Escolha o modo de jogo")
			form.td(e, height=80)
			
			form.tr()
			e = gui.Button("1 jogador")
			e.connect(gui.CLICK, self.umJogadorEventHandler, None)
			form.td(e)

			b = gui.Button("2 jogadores")
			b.connect(gui.CLICK, self.doisJogadoresEventHandler, None)
			form.tr()
			form.td(b, height=60)

			c = gui.Button("0 jogadores")
			c.connect(gui.CLICK, self.zeroJogadoresEventHandler, None)
			form.tr()
			form.td(c)
			
			c = gui.Container(align=-1,valign=-1)
			c.add(form,70,80)
			self.app.init(c)
	
		elif self.estadoJogo == 2:
			formf=gui.Form()
			self.app = gui.App()
			form = gui.Table()
			form.tr()
			e = gui.Button("New Game")
			e.connect(gui.CLICK, self.novoJogoEventHandler, None)
			form.td(e)
		
			c = gui.Container(align=-1,valign=-1)
			c.add(form, 1, 1)
		
			self.app.init(c)
			self.tab = Tabuleiro(pygame)

		elif self.estadoJogo == 1:
			self.app = gui.App()
			c = gui.Container(align=-1,valign=-1)

			vs = gui.Image("vs.png", width=160, height=160)
			c.add(vs, 75, 225)		
			
			computador = gui.List(width=125, height=155)
			computador.add("Pontuacao", value=0)
			computador.add("Mobilidade", value=1)
			computador.add("Captura", value=2)
			computador.add("Posicionamento", value=3)
			computador.add("HeuristicaX", value=4)
			computador.add("HeuristicaY", value=5)
			computador.add("HeuristicaZ", value=6)
			self.heuristica1 = computador
			c.add(computador, 95, 100)

			e = gui.Button("Voltar")
			e.connect(gui.CLICK, self.novoJogoEventHandler, None)
			c.add(e, 5, 5)
		
			form = gui.Table()
			form.tr()
			form.td(gui.Label("Computador", color=(127,32,50)), width=128)
			c.add(form, 95, 60)

			a = gui.Label("HEURISTICA", color=(127,32,50))
			c.add(a, 110, 30)

			self.app.init(c)

		elif self.estadoJogo == 3:
			self.app = gui.App()
			c = gui.Container(align=-1,valign=-1)

			vs = gui.Image("vs.png", width=160, height=160)
			c.add(vs, 75, 225)		
			
			jogador1 = gui.List(width=125, height=155)
			jogador1.add("Pontuacao", value=0)
			jogador1.add("Mobilidade", value=1)
			jogador1.add("Captura", value=2)
			jogador1.add("Posicionamento", value=3)
			jogador1.add("HeuristicaX", value=4)
			jogador1.add("HeuristicaY", value=5)
			jogador1.add("HeuristicaZ", value=6)
			self.heuristica1 = jogador1
			c.add(jogador1, 15, 110)

			jogador2 = gui.List(width=125, height=155)
			jogador2.add("Pontuacao", value=0)
			jogador2.add("Mobilidade", value=1)
			jogador2.add("Captura", value=2)
			jogador2.add("Posicionamento", value=3)
			jogador2.add("HeuristicaX", value=4)
			jogador2.add("HeuristicaY", value=5)
			jogador2.add("HeuristicaZ", value=6)
			self.heuristica2 = jogador2
			c.add(jogador2, 200, 110)

			e = gui.Button("Voltar")
			e.connect(gui.CLICK, self.novoJogoEventHandler, None)
			c.add(e, 5, 5)
		
			form = gui.Table()
			form.tr()
			form.td(gui.Label("Jogador 1", color=(127,32,50)), width=128)
			form.td(gui.Label("Jogador 2", color=(127,32,50)), width=240)
			c.add(form, 15, 70)

			a = gui.Label("HEURISTICAS", color=(127,32,50))
			c.add(a, 115, 30)

			self.app.init(c)

    def loop(self):
		if self.estadoJogo == 2:
			self.tab.refresh()
			
		self.app.paint()
		pygame.display.flip()
		self.input(pygame.event.get())

game = Game()

