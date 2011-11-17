#!/usr/bin/env python
import os, sys, copy
from peca import *
import time

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
            print "Fim do Jogo"            
            return 1
        
    def initPecas(self):
        for i in range(8):
            for j in range (8):
                self.tabuleiro[i][j] = Peca()
	
	pecas = [self.tabuleiro[3][3], self.tabuleiro[4][3], self.tabuleiro[4][4], self.tabuleiro[3][4]]

	for peca in pecas:
            peca.estado = self.alternador()

	self.pontuacao()
    
    def click(self, x, y):

        if x < self.offset[0] or x > self.size[0] + self.offset[0]:
            return
        if y < self.offset[1] or y > self.size[1] + self.offset[1]:
            return

        peca = self.tabuleiro[self.map(x, 0)][self.map(y, 1)]

        if peca.estado == 0 and self.jogadaValida(self.map(x, 0), self.map(y, 1)) == 1:
            peca.estado = self.alternador()
        else:
            peca.estado = peca.estado
        self.fimJogo()
        self.pontuacao()
        

    def jogadaValida(self, i, j): #0:jogadaInvalida, 1:jogadaValida	
	todosVirar = []
	virar = []
	jogadaValida = 0
	# PERCORRENDO COLUNAS
	for a in range(8 - i - 1): # Para direita
		col = i + a + 1
		peca = self.tabuleiro[col][j]
		resposta = self.verificaJogada(peca, a)
		if resposta == 1:
			todosVirar.append(virar)
			jogadaValida = 1
			break
		if resposta == 2:
			break
		virar.append(peca)

	virar = []
	for a in range(i): # Para esquerda
		col = i - (a + 1)
		peca = self.tabuleiro[col][j]
		resposta = self.verificaJogada(peca, a)
		if resposta == 1:
			todosVirar.append(virar)
			jogadaValida = 1
			break
		if resposta == 2:
			break
		virar.append(peca)
	
	virar = []
	# PERCORRENDO LINHAS
	for a in range(8 - j - 1): # Para baixo
		lin = j + a + 1
		peca = self.tabuleiro[i][lin]
		resposta = self.verificaJogada(peca, a)
		if resposta == 1:
			todosVirar.append(virar)
			jogadaValida = 1
			break
		if resposta == 2:
			break
		virar.append(peca)
	virar = []
	for a in range(j): # Para cima
		lin = j - (a + 1)
		peca = self.tabuleiro[i][lin]
		resposta = self.verificaJogada(peca, a)
		if resposta == 1:
			todosVirar.append(virar)
			jogadaValida = 1
			break
		if resposta == 2:
			break
		virar.append(peca)

	# PERCORRENDO DIAGONAIS
	if j > i: # A diogonal sera percorrida ate no maximo a distancia mais proxima a borda (horizontal ou vertical)
		indD = 8 - j - 1
	else:
		indD = 8 - i - 1
	virar = []
	for a in range(indD): # Para baixo, direita
		lin = j + a + 1
		col = i + a + 1
		peca = self.tabuleiro[col][lin]
		resposta = self.verificaJogada(peca, a)
		if resposta == 1:
			todosVirar.append(virar)
			jogadaValida = 1
			break
		if resposta == 2:
			break
		virar.append(peca)
	virar = []
	for a in range(indD): # Para cima, direita
		lin = j - (a + 1)
		col = i + a + 1
		peca = self.tabuleiro[col][lin]
		resposta = self.verificaJogada(peca, a)
		if resposta == 1:
			todosVirar.append(virar)
			jogadaValida = 1
			break
		if resposta == 2:
			break
		virar.append(peca)
	virar = []
	for a in range(indD): # Para baixo, esquerda
		lin = j + a + 1
		col = i - (a + 1)
		peca = self.tabuleiro[col][lin]
		resposta = self.verificaJogada(peca, a)
		if resposta == 1:
			todosVirar.append(virar)
			jogadaValida = 1
			break
		if resposta == 2:
			break
		virar.append(peca)
	virar = []
	for a in range(indD): # Para cima, esquerda
		lin = j - (a + 1)
		col = i - (a + 1)
		peca = self.tabuleiro[col][lin]
		resposta = self.verificaJogada(peca, a)
		if resposta == 1:
			todosVirar.append(virar)
			jogadaValida = 1
			break
		if resposta == 2:
			break
		virar.append(peca)

	# Se a jogada for valida, da o flip nas pecas para a cor do jogador corrente
	if jogadaValida == 1:
		if self.last == 1:
			cor = 2
		else:
			cor = 1
		for t in todosVirar:
			for t0 in t:
				t0.estado = cor
	else:
		print "Erro: Jogada Invalida"		
		
	return jogadaValida

    def verificaJogada(self, peca, a): # 1:jogadaValida, 0:continua, 2:para
	if peca.estado == 0:
		return 2

	# Se a peca que esta percorrendo e a mesma do jogador atual e ha pelo menos uma peca entre as duas
	if peca.estado != self.last:
		if a > 0:
			return 1
		else:
			return 2

	return 0

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
