#!/usr/bin/env python
import os, sys, copy
from peca import *

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
    tempo = 0
    tempoVermelho = 0
    tempoPreto = 0
    tempoAdicionar = 1.9
    
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

        #proximo jogador
        peca = Peca()
        proximo = self.font.render(" Proximo ",1,(0,0,0))
        screen.blit(proximo,(25,30))
        if self.last == 2:
                self.tempoVermelho = self.tempoVermelho + self.tempoAdicionar
                peca.estado = 1
        elif self.last == 1:
                self.tempoPreto = self.tempoPreto + self.tempoAdicionar
                peca.estado = 2 
        screen.blit(peca.img(), (0, 25))
        
        #escreve a pontuacao na tela
        ren = self.font.render(" Pontuacao",1,(0,0,0))
        screen.blit(ren,(120,0))

        #peca vermelha
        peca.estado = 1 
        pontVerm = self.font.render(":" + str(self.pontosVermelho),1,(255,0,0))
        screen.blit(pontVerm,(150,30))
        screen.blit(peca.img(), (120, 20))

        #peca preta
        peca.estado = 2
        pontPreto = self.font.render(":" + str(self.pontosPreto),1,(0,0,0))
        screen.blit(pontPreto,(215, 30))
        screen.blit(peca.img(), (185, 20))

        #cronometro
        cron = self.font.render(" Tempo",1,(0,0,0))
        screen.blit(cron,(250,0))
        segundos = int(round(self.tempo/1000))
        minutos = int(round(segundos/60))
        segundos = int(round(segundos % 60))
        
        cronometro = ('%02d:%02d' % (minutos, segundos))
        tempoTela = self.font.render(str(cronometro), 1, (0,0,0))
        screen.blit(tempoTela, (260, 30))


        for i in range(8):
            for j in range(8):
                item = self.tabuleiro[i][j]
                if item.estado != 0:
                    newsurface = item.img()
                    screen.blit(newsurface, (i*41 + 5 + self.offset[0], j*41 + 5 + self.offset[1]))

        self.tempo = self.tempo + self.tempoAdicionar
        
    def isPassaVez(self, tabuleiroFimJogo):
        for i in range(8):
            for j in range(8):
                item = tabuleiroFimJogo[i][j]
                if (item.estado == 0):
                    #jogador atual ainda tem jogada valida
                    if(self.jogadaValida(i, j, tabuleiroFimJogo, 1)):       
                        return 0
        return 1
 
    def isFimJogo(self, tabuleiroFimJogo, alterna):
        fim = 1         # 1 = fim de jogo; 0 = continua jogo
        todosVermelho = 1       # 1 = nao existe peca preta, vermelho ganhou
        todosPreto = 1          # 1 = nao existe peca vermelha, preto ganhou

        # Caso base, todas as posicoes do tabuleiro ocupadas, ou so pecas de um jogador
        for i in range(8):
            for j in range(8):
                item = tabuleiroFimJogo[i][j]
                if item.estado == 0:
                    fim = 0
                elif item.estado == 1:
                    todosPreto = 0
                elif item.estado == 2:
                    todosVermelho = 0
        
        if (todosPreto or todosVermelho):
            return 1

        if (not(fim)):
            fim = 1
            # Verificacao de passar a vez
            if not self.isPassaVez(tabuleiroFimJogo):
                return 0
            
            #Se chegou aqui significa que o jogador atual nao tem mais jogadas validas                        
            print " Passou a vez "
            self.alternador()
            if self.isPassaVez(tabuleiroFimJogo):
                return 1
            if alterna:
                self.alternador()
        return fim
        
    def fimJogo(self, tabuleiroFimJogo):        
        if (self.isFimJogo(tabuleiroFimJogo, 1)):
            print " Fim do Jogo "            
            self.pontuacao()
            if self.pontosVermelho > self.pontosPreto:
                print " Vermelho ganhou "
            elif self.pontosVermelho < self.pontosPreto:
                print " Preto ganhou "
            else:
                print " Empate "
                
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

        mapX = self.map(x,0)
        mapY = self.map(y,1)
        
        peca = self.tabuleiro[mapX][mapY]

        if (not peca.estado) and self.jogadaValida(mapX, mapY, self.tabuleiro, 0):
            peca.estado = self.alternador()
        
        self.fimJogo(self.tabuleiro)
        self.pontuacao()
        
        

    def jogadaValida(self, i, j, tabuleiroFimJogo, verifica): #0:jogadaInvalida, 1:jogadaValida 
        todosVirar = []
        virar = []
        jogadaValida = 0
        # PERCORRENDO COLUNAS
        for a in range(7 - i): # Para direita
            col = i + a + 1
            peca = tabuleiroFimJogo[col][j]
            resposta = self.verificaJogada(peca, a)
            if resposta == 1:
                if (not(verifica)):
                    todosVirar.append(virar)
                jogadaValida = 1
                break
            elif resposta == 2:
                break
            else:
                virar.append(peca)

        virar = []
        for a in range(i): # Para esquerda
            col = i - (a + 1)
            peca = tabuleiroFimJogo[col][j]
            resposta = self.verificaJogada(peca, a)
            if resposta == 1:
                if (not(verifica)):
                    todosVirar.append(virar)
                jogadaValida = 1
                break
            if resposta == 2:
                break
            if (not(verifica)):
                virar.append(peca)
        
        virar = []
        # PERCORRENDO LINHAS
        for a in range(7 - j): # Para baixo
            lin = j + a + 1
            peca = tabuleiroFimJogo[i][lin]
            resposta = self.verificaJogada(peca, a)
            if resposta == 1:
                if (not(verifica)):
                    todosVirar.append(virar)
                jogadaValida = 1
                break
            if resposta == 2:
                break
            if (not(verifica)):
                virar.append(peca)

        virar = []
        for a in range(j): # Para cima
            lin = j - (a + 1)
            peca = tabuleiroFimJogo[i][lin]
            resposta = self.verificaJogada(peca, a)
            if resposta == 1:
                if (not(verifica)):
                    todosVirar.append(virar)
                jogadaValida = 1
                break
            if resposta == 2:
                break
            if (not(verifica)):
                virar.append(peca)

        # PERCORRENDO DIAGONAIS
        indD = 7
        virar = []
        if (j < 7 and i < 7):
            for a in range(indD): # Para baixo, direita
                lin = j + a + 1
                col = i + a + 1
                if(lin > 7 or col > 7 or lin < 0 or col < 0):
                    break
                peca = tabuleiroFimJogo[col][lin]
                resposta = self.verificaJogada(peca, a)
                if resposta == 1:
                    if (not(verifica)):
                        todosVirar.append(virar)
                    jogadaValida = 1
                    break
                if resposta == 2:
                    break
                if (not(verifica)):
                    virar.append(peca)
            virar = []
            
        if (i < 7):
            for a in range(indD): # Para cima, direita
                lin = j - (a + 1)
                col = i + a + 1
                if(lin > 7 or col > 7 or lin < 0 or col < 0):
                    break
                peca = tabuleiroFimJogo[col][lin]
                resposta = self.verificaJogada(peca, a)
                if resposta == 1:
                    if (not(verifica)):
                        todosVirar.append(virar)
                    jogadaValida = 1
                    break
                if resposta == 2:
                    break
                if (not(verifica)):
                    virar.append(peca)
            virar = []

        if (j < 7):
            for a in range(indD): # Para baixo, esquerda
                lin = j + a + 1
                col = i - (a + 1)
                if(lin > 7 or col > 7 or lin < 0 or col < 0):
                    break
                peca = tabuleiroFimJogo[col][lin]
                resposta = self.verificaJogada(peca, a)
                if resposta == 1:
                    if (not(verifica)):
                        todosVirar.append(virar)
                    jogadaValida = 1
                    break
                if resposta == 2:
                    break
                if (not(verifica)):
                    virar.append(peca)
            virar = []

        for a in range(indD): # Para cima, esquerda
            lin = j - (a + 1)
            col = i - (a + 1)
            if(lin > 7 or col > 7 or lin < 0 or col < 0):
                break
            peca = tabuleiroFimJogo[col][lin]
            resposta = self.verificaJogada(peca, a)
            if resposta == 1:
                if (not(verifica)):
                    todosVirar.append(virar)
                jogadaValida = 1
                break
            if resposta == 2:
                break
            if (not(verifica)):
                virar.append(peca)


        # Se a jogada for valida, da o flip nas pecas para a cor do jogador corrente
        if ((jogadaValida == 1) and (not(verifica))):
            for t in todosVirar:
                for t0 in t:
                    t0.flip()
        elif((jogadaValida != 1) and (not(verifica))):
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
                    
	# Funcao que cria a arvore do alfa-beta prunning
	def minimax(self, tabuleiroMiniMax, profundidade):
	
		if (profundidade == 0):
			return self.funcaoAvaliacao(tabuleiroMiniMax)
	
		# Procuro por uma peca do jogador adversario (self.last)
		for i in range(8):
		 		for j in range(8):
					item = tabuleiroMiniMax[i][j]
					# Local vazio
					if (item.estado == 0):
						break

					# Peca do adversario
					elif (item.estado == self.last):
			
						# percorro a linha acima, da esquerda pra direita
						if (i > 0):
							linha = i - 1
							for a in range(-1, 1):
								coluna = j + a
								novoTab = copy.deepcopy(tabuleiroMiniMax)
								item = novoTab[linha][coluna]
								if (coluna >= 0 and coluna <= 7 and item.estado == 0):
									jogVal = self.jogadaValida(linha, coluna, novoTab, 0)
									if (jogVal):
										fimJogo = self.isFimJogo(novoTab, 0)
										if (not(fimJogo)):
											minimax(novoTab, profundidade - 1)
									
			
						# percorro a linha abaixo, da esquerda pra direita
						if (i < 7):
							linha = i + 1
							for a in range(-1, 1):
								coluna = j + a
								novoTab = copy.deepcopy(tabuleiroMiniMax)
								item = novoTab[linha][coluna]
								if (coluna >= 0 and coluna <= 7 and item.estado == 0):
									jogVal = self.jogadaValida(linha, coluna, novoTab, 0)
									if (jogVal):
										fimJogo = self.isFimJogo(novoTab, 0)
										if (not(fimJogo)):
											minimax(novoTab, profundidade - 1)
			
						# percorro a linha da peca, da esquerda pra direita
						linha = i
						for a in range(-1, 2, 2):
							novoTab = copy.deepcopy(tabuleiroMiniMax)
							item = novoTab[linha][coluna]
							if (coluna >= 0 and coluna <= 7 and item.estado == 0):
								jogVal = self.jogadaValida(linha, coluna, novoTab, 0)
								if (jogVal):
										fimJogo = self.isFimJogo(novoTab, 0)
										if (not(fimJogo)):
											minimax(novoTab, profundidade - 1)			

					# Peca do jogador atual
					else:
						break                    

        
    def map(self, x, i):
        return int(round((x-self.offset[i])/41,0))
        
    def alternador(self):
        if self.last == 1:
            self.last = 2
            self.tempo = self.tempoVermelho
        else:
            self.last = 1
            self.tempo = self.tempoPreto
        return self.last
