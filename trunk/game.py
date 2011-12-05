#!/usr/bin/env python
import os, sys
from tabuleiro import *
import pygame
from pygame.locals import *
from pgu import gui

class Game:
    tab = ''
    estadoJogo = 0
    inicializado = 0
    ai1 = -1
    ai2 = -2
    #TABELA DE ESTADOS################################################################################################    
    ##################################################################################################################
    #    VALOR     #                                       SIGNIFICADO                                               #
    ##################################################################################################################
    #     0        #  Selecionar 2, 1 ou 0 jogadores                                                                 #
    #     1        #  Selecionar heuristica para a AI do modo de 1 jogador                                           #
    #     2        #  Jogo iniciado com 2 jogadores humanos                                                          #
    #     3        #  Selecionar as duas heuristicas para as AIs do modo de 0 jogadores humanos                      #
    #     4        #  Jogo iniciado com 1 AI vs. 1 Humano                                                            #
    #     5        #  Jogo iniciado com AI vs. AI                                                                    #
    ##################################################################################################################
    
    #### FSM ##############################################
    #    ( 1 ) ----------> ( 4 )                          #
    #     /\                                              #
    #     |                                               #
    #     |                                               #
    #     |                                               #
    #   ( 0 ) ---------->  ( 3 ) -----------> ( 5 )       #
    #     |                                               #
    #     |                                               #
    #     |                                               #
    #    \/                                               #
    #   ( 2 )                                             #
    #######################################################

    
    def input(self,events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                # O tabuleiro somente aceita acao de click do usuario se nao for IA versus IA
                if self.estadoJogo == 2 or self.estadoJogo == 4:
                    self.botaoHabilitado = self.tab.click(event.dict['pos'][0],event.dict['pos'][1])
                
                # Pegando a heuristica escolhida para o computador(es)
                if (self.estadoJogo == 1 or (self.estadoJogo == 3 and self.heuristica2.value != None)) and self.heuristica1.value != None:
                    # Mapeamento (posicao x e y) da botao versus neste estado
                    if self.isClickPlayGame(event.dict['pos'][0], event.dict['pos'][1]):                       
                        self.ai1 = self.heuristica1.value
                        self.inicializado = 0
                        
                        if self.estadoJogo == 1:
                            self.estadoJogo = 4
                        else: # Se for IA vs IA pega a heuristica do segundo computador
                            self.estadoJogo = 5
                            self.ai2 = self.heuristica2.value
                        
        # Simplesmente dispara o evento para aplicacao ou a fecha se o usuario requisitou isso                
        for event in events: 
            if event.type == QUIT: 
                sys.exit(0)
            else:
                self.app.event(event)   

    def isClickPlayGame(self, x, y): # Mapeia o botao 'Play Game'
        return x >= 95 and x <= 220 and y >= 330 and y <= 370

    def novoJogoEventHandler(self, event):
        self.novaEscolha(0)

    def umJogadorEventHandler(self, event):
        self.novaEscolha(1)

    def doisJogadoresEventHandler(self, event):
        self.novaEscolha(2)
        
    def zeroJogadoresEventHandler(self, event):     
        self.novaEscolha(3)       
        
    def passarVezEventHandler(self, event):
        self.tab.alternador()
    
    def novaEscolha(self, estado):
        self.estadoJogo = estado
        self.inicializado = 0
        self.ai1 = -1
        self.ai2 = -1   

    def __init__(self): # Instancia a aplicacao
        pygame.init()
        window = pygame.display.set_mode((329, 389), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption('Reversi')
        while True:
            self.inicializa()
            self.inicializado = 1
            while self.inicializado:
                window.fill((255, 255, 255))
                self.loop()

    def inicializa(self): # Carrega a tela correspondente ao estado
        self.app = gui.App()
        c = gui.Container(align=-1,valign=-1)
        
        if self.estadoJogo == 0 or self.estadoJogo == 1 or self.estadoJogo == 3: # Nos estados que nao sao o tabuleiro coloque a arte padrao
            im = gui.Image("img/titulo.png")
            c.add(im, 0, 0)
            im = gui.Image("img/fundo.png")
            c.add(im, 0, 213)
            im = gui.Image("img/fundo.png")
            c.add(im, 0, 361)
        
        if self.estadoJogo == 0: # Tela inicial          
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

            d = gui.Button("0 jogadores")
            d.connect(gui.CLICK, self.zeroJogadoresEventHandler, None)
            form.tr()
            form.td(d)
            
            c.add(form, 70, 80)

        elif self.estadoJogo == 2 or self.estadoJogo == 4 or self.estadoJogo == 5: # Tela do tabuleiro          
            form = gui.Table()
            form.tr()
            e = gui.Button("Novo Jogo")
            e.connect(gui.CLICK, self.novoJogoEventHandler, None)
            form.td(e)
    
            c.add(form, 1, 1)

            self.tab = Tabuleiro(pygame, self.ai1, self.ai2)

        elif self.estadoJogo == 1 or self.estadoJogo == 3: # Escolha da heuristica do computador
            e = gui.Button("Voltar")
            e.connect(gui.CLICK, self.novoJogoEventHandler, None)
            c.add(e, 5, 5)
            
            a = gui.Label("HEURISTICA / NIVEL", color=(0, 0, 0))
            c.add(a, 85, 85)
            
            pg = gui.Image("img/playgame.png", width=125, height=40)
            c.add(pg, 95, 330)
            
            form = gui.Table()
            form.tr()
            if self.estadoJogo == 1: # Contra somente 1 jogador humano
                form.td(gui.Label("Computador", color=(0, 0, 0)), width=100)
                c.add(form, 90, 120)
                
                pg = gui.Image("img/pecapreta.png")
                c.add(pg, 195, 112)
                
                self.heuristica1 = self.listaHeuristicas()
                c.add(self.heuristica1, 95, 150)
            else: # Nenhuma jogador humano
                form.td(gui.Label("Jogador", color=(0, 0, 0)), width=100)
                form.td(gui.Label("Jogador", color=(0, 0, 0)), width=280)
                pg = gui.Image("img/pecavermelha.png")
                c.add(pg, 92, 112)
                
                pg = gui.Image("img/pecapreta.png")
                c.add(pg, 280, 112)
                
                c.add(form, 5, 120)
                
                self.heuristica1 = self.listaHeuristicas()
                c.add(self.heuristica1, 5, 150)
           
                self.heuristica2 = self.listaHeuristicas()
                c.add(self.heuristica2, 190, 150)

        self.app.init(c)

    def listaHeuristicas(self): # Lista de Heuristicas do jogo
        heuristicas = gui.List(width=125, height=155)
        heuristicas.add("Easy", value=4)
        heuristicas.add("Normal", value=5)
        heuristicas.add("Expert", value=6)
        heuristicas.add("----------", value=10)
        heuristicas.add("Numero Peca", value=0)
        heuristicas.add("Mobilidade", value=1)
        heuristicas.add("Captura", value=2)
        heuristicas.add("Peso Posicao", value=3)
        
        return heuristicas

    def loop(self): # Fica reescrevendo a tela e capturando evento baseado no estado do jogo
        if self.estadoJogo == 2 or self.estadoJogo == 4 or self.estadoJogo == 5:
            self.tab.refresh()
                
        self.app.paint()
        pygame.display.flip()
        self.input(pygame.event.get())

game = Game()