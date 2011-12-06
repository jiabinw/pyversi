#!/usr/bin/env python
import os, sys, copy
import time
from peca import *
from numeroPeca import *
from mobilidade import *
from pesoPosicao import *
from captura import *
from nivelFacil import *
from nivelMedio import *
from nivelDificil import *

class Tabuleiro:
    pygame = 0
    ImgSurface = 0
    offset = (0,60)
    size = (341,341)
    tabuleiro = []
    IMGPATH = os.path.join("img", "tabuleiro.png")
    pontosVermelho = 0
    pontosPreto = 0
    last = 2
    atual = 1
    tempo = 0
    tempoVermelho = 0
    tempoPreto = 0
    tempoAdicionar = 1.9
    ai = 0
    human = 0
    fim = 0
    heuristicas = []
    start_time = 0
    end_time = 0
    elapsedTimeRed = 0
    elapsedTimeBlack = 0
    
    def __init__(self, game, ai1 = -1, ai2 = -1):
        self.font = pygame.font.SysFont("Courier New", 18)
        self.pygame = game       
        self.ImgSurface = self.pygame.image.load(self.IMGPATH)
        row = [0] * 8        
        
        for item in row:
            self.tabuleiro.append(copy.deepcopy(row))
        
        #print ai1, ai2
        self.heuristicas = []
        
        if ai1 != -1:
            self.ai = 1
            if ai1 == 0:
                self.heuristicas.append(NumeroPeca())
            elif ai1 == 1:
                self.heuristicas.append(Mobilidade())
            elif ai1 == 2:
                self.heuristicas.append(Captura())
            elif ai1 == 3:
                self.heuristicas.append(PesoPosicao())
            elif ai1 == 4:
                self.heuristicas.append(NivelFacil())
            elif ai1 == 5:
                self.heuristicas.append(NivelMedio())
            elif ai1 == 6:
                self.heuristicas.append(NivelDificil())
        if ai1 != -1 and ai2 != -1:
            self.ai = 1
            if ai2 ==0:
                self.heuristicas.append(NumeroPeca())
            elif ai2 == 1:
                self.heuristicas.append(Mobilidade())
            elif ai2 == 2:
                self.heuristicas.append(Captura())
            elif ai2 == 3:
                self.heuristicas.append(PesoPosicao())
            elif ai2 == 4:
                self.heuristicas.append(NivelFacil())
            elif ai2 == 5:
                self.heuristicas.append(NivelMedio())
            elif ai2 == 6:
                self.heuristicas.append(NivelDificil())
        else:
            self.human = 1
            
        self.start_time = time.time()
        self.initPecas()
            

    def refresh(self):	
        colorFlag = self.last
        if self.atual == 1:
          self.elapsedTimeRed = time.time()               
        else:
          self.elapsedTimeBlack = time.time()
          
        if not self.human and not self.fim:                 
            self.tabuleiro = self.minimax(self.tabuleiro, 4, 1, 1, self.atual, self.heuristicas[self.atual - 1], float("-inf"), float("inf"))[1]
            self.alternador()
            self.fim = self.fimJogo(self.tabuleiro, 1, self.atual)
            self.pontuacao()
        
        if self.atual != colorFlag:       
          if self.atual == 1:
            self.elapsedTimeBlack = time.time()
          else:
            self.elapsedTimeRed = time.time()
            
        screen = self.pygame.display.get_surface()        
        screen.blit(self.ImgSurface, self.offset)

        #proximo jogador
        peca = Peca()
        proximo = self.font.render(" Proximo ", 1, (0, 0, 0))
        screen.blit(proximo,(25, 30))
        if self.last == 2:
                self.end_time = time.time()             
                self.elapsedTimeBlack = self.end_time - self.elapsedTimeBlack           
                self.tempoPreto = self.elapsedTimeBlack + self.tempoPreto               
                peca.estado = 2 
        elif self.last == 1:
                self.end_time = time.time()
                self.elapsedTimeRed = self.end_time - self.elapsedTimeRed                       
                self.tempoVermelho = self.elapsedTimeRed + self.tempoVermelho                   
                peca.estado = 1

        screen.blit(peca.img(), (0, 25))
        
        #escreve a pontuacao na tela
        ren = self.font.render(" Pontuacao", 1, (0, 0, 0))
        screen.blit(ren, (120, 0))

        #peca vermelha
        peca.estado = 1 
        pontVerm = self.font.render(":" + str(self.pontosVermelho), 1, (255, 0, 0))
        screen.blit(pontVerm,(150, 30))
        screen.blit(peca.img(), (120, 20))

        #peca preta
        peca.estado = 2
        pontPreto = self.font.render(":" + str(self.pontosPreto), 1, (0, 0, 0))
        screen.blit(pontPreto,(215, 30))
        screen.blit(peca.img(), (185, 20))

        #cronometro
        cron = self.font.render(" Tempo", 1, (0, 0, 0))
        screen.blit(cron,(250,0))
        #segundos = int(round(self.tempo / 1000))
        #minutos = int(round(segundos / 60))
        #segundos = int(round(segundos % 60))
              
        
        self.end_time = time.time()
        
        cronometro = self.end_time - self.start_time
        cronometro = ('%02d s' % (cronometro))
        
        #print cronometro
        tempoTela = self.font.render(str(cronometro), 1, (0,0,0))
        screen.blit(tempoTela, (260, 30))

        for i in range(8):
            for j in range(8):
                item = self.tabuleiro[i][j]
                if item.estado != 0:
                    newsurface = item.img()
                    screen.blit(newsurface, (i*41 + 5 + self.offset[0], j*41 + 5 + self.offset[1]))

        self.tempo = self.tempo + self.tempoAdicionar
        
    def isPassaVez(self, tabuleiroFimJogo, jogadorAtual):
        for i in range(8):
            for j in range(8):
                item = tabuleiroFimJogo[i][j]
                if (item.estado == 0):
                    #jogador atual ainda tem jogada valida
                    if(self.jogadaValida(i, j, tabuleiroFimJogo, 1, jogadorAtual)):       
                        return 0
        return 1
 
    def isFimJogo(self, tabuleiroFimJogo, alterna, jogadorAtual):
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
            if not self.isPassaVez(tabuleiroFimJogo, jogadorAtual):
                return 0
            
            #Se chegou aqui significa que o jogador atual nao tem mais jogadas validas                        
            print " Passou a vez ", jogadorAtual
            if jogadorAtual == 1:
                player = 2
            else:
                player = 1
            if self.isPassaVez(tabuleiroFimJogo, player):
                return 1
            if alterna:
                self.alternador()
            return 0
        else:
            return 1
        
        
    def fimJogo(self, tabuleiroFimJogo, alterna,  jogadorAtual):        
        if (self.isFimJogo(tabuleiroFimJogo, alterna, jogadorAtual)):
            print " Fim do Jogo "            
            self.pontuacao()
            if self.pontosVermelho > self.pontosPreto:
                print " Vermelho ganhou "
            elif self.pontosVermelho < self.pontosPreto:
                print " Preto ganhou "
            else:
                print " Empate "
            print "Red Time", self.tempoVermelho
            print "Black Time", self.tempoPreto
            return 1
        return 0
        
                
    def initPecas(self):
        for i in range(8):
            for j in range (8):
                self.tabuleiro[i][j] = Peca()
        
        pecas = [self.tabuleiro[3][3], self.tabuleiro[4][3], self.tabuleiro[4][4], self.tabuleiro[3][4]]

        for peca in pecas:
            peca.estado = self.alternador()
        #self.alternador()
        #
        #self.tabuleiro = self.minimax(self.tabuleiro, 4, 1, 1, self.atual, self.heuristicas[0], float("-inf"), float("inf"))[1]
        #self.alternador()
        #self.fim = self.fimJogo(self.tabuleiro, self.atual)
        #self.pontuacao()
        
    
    def click(self, x, y):
        if x < self.offset[0] or x > self.size[0] + self.offset[0]:
            return
        if y < self.offset[1] or y > self.size[1] + self.offset[1]:
            return

        mapX = self.map(x,0)
        mapY = self.map(y,1)
        
        peca = self.tabuleiro[mapX][mapY]

        if (not peca.estado) and self.jogadaValida(mapX, mapY, self.tabuleiro, 0, self.atual):
            peca.estado = self.alternador() 
            self.fim = self.fimJogo(self.tabuleiro, 1, self.atual) 
            self.pontuacao()
            
            if self.ai and self.human and not self.fim and not peca.estado == self.atual:
                self.tabuleiro = self.minimax(self.tabuleiro, 4, 1, 1, self.atual, self.heuristicas[0], float("-inf"), float("inf"))[1]
                self.pontuacao()
                self.alternador()
                self.fim = self.fimJogo(self.tabuleiro, 0, self.atual)
                while self.isPassaVez(self.tabuleiro, self.atual) and not self.fim:
                    self.tabuleiro = self.minimax(self.tabuleiro, 4, 1, 1, self.last, self.heuristicas[0], float("-inf"), float("inf"))[1]
                    self.pontuacao()
                    self.fim = self.fimJogo(self.tabuleiro, 0, self.last)

                #while True:
                #    print 'iterou'
                #    if not self.isPassaVez(self.tabuleiro, self.atual):
                #        self.tabuleiro = self.minimax(self.tabuleiro, 4, 1, 1, self.atual, self.heuristicas[0], float("-inf"), float("inf"))[1]
                #   
                #    self.alternador()
                #    
                #    
                #    if self.isPassaVez(self.tabuleiro, self.atual) == 0 or self.isFimJogo(self.tabuleiro, 0, self.atual):
                #        break
                #    
                #    
                #    self.fim = self.fimJogo(self.tabuleiro, self.atual)
                #    self.pontuacao()
                
                

    def jogadaValida(self, i, j, tabuleiroFimJogo, verifica, jogadorAtual): #0:jogadaInvalida, 1:jogadaValida 
        todosVirar = []
        virar = []
        jogadaValida = 0
        
        # PERCORRENDO COLUNAS
        for a in range(7 - i): # Para direita
            col = i + a + 1
            peca = tabuleiroFimJogo[col][j]
            resposta = self.verificaJogada(peca, a, jogadorAtual)
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
            resposta = self.verificaJogada(peca, a, jogadorAtual)
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
            resposta = self.verificaJogada(peca, a, jogadorAtual)
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
            resposta = self.verificaJogada(peca, a, jogadorAtual)
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
                resposta = self.verificaJogada(peca, a, jogadorAtual)
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
                resposta = self.verificaJogada(peca, a, jogadorAtual)
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
                resposta = self.verificaJogada(peca, a, jogadorAtual)
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
            resposta = self.verificaJogada(peca, a, jogadorAtual)
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
        #elif((jogadaValida != 1) and (not(verifica))):
            #print "Erro: Jogada Invalida"           
                
        return jogadaValida


    def verificaJogada(self, peca, a, jogadorAtual): # 1:jogadaValida, 0:continua, 2:para
        if peca.estado == 0:
            return 2

        # Se a peca que esta percorrendo e a mesma do jogador atual e ha pelo menos uma peca entre as duas
        if peca.estado == jogadorAtual:
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
                    

    def proxPeca(self, i,j, tabuleiro, jogador):
        for y in range(j+1, 8):
            if tabuleiro[i][y].estado == jogador:
                return (i,y)
        
        for x in range (i+1, 8):
            for y in range(8):
                if tabuleiro[x][y].estado == jogador:
                    return (x,y)
        return (-1,-1)
            

    def proximaJogada(self, tabuleiro, mapeamento, jogadorAtual):
        ultimaLinha = mapeamento[8][0]
        ultimaColuna = mapeamento[8][1]
        
        oponente = 0
        if(jogadorAtual == 1):
            oponente = 2
        else:
            oponente = 1      
         
        # Procuro por uma peca do jogador adversario (oponente)
        if not tabuleiro[ultimaLinha][ultimaColuna].estado == oponente:
            (ultimaLinha, ultimaColuna) = self.proxPeca(ultimaLinha, ultimaColuna, tabuleiro, oponente)
        
        while not (ultimaLinha, ultimaColuna) == (-1,-1):                
                # percorro a linha acima, da esquerda pra direita
                if (ultimaLinha > 0):
                    linha = ultimaLinha - 1
                    for a in range(-1, 2):
                        coluna = ultimaColuna + a
                        if (coluna >= 0 and coluna <= 7 and tabuleiro[linha][coluna].estado == 0 and mapeamento[linha][coluna] == 0):
                            mapeamento[linha][coluna] = 1
                            mapeamento[8][0] = ultimaLinha
                            mapeamento[8][1] = ultimaColuna
                            return (linha, coluna)
                           
                # percorro a linha abaixo, da esquerda pra direita
                if (ultimaLinha < 7):
                    linha = ultimaLinha + 1
                    for a in range(-1, 2):
                        coluna = ultimaColuna + a
                        if (coluna >= 0 and coluna <= 7 and tabuleiro[linha][coluna].estado == 0 and mapeamento[linha][coluna] == 0):
                            mapeamento[linha][coluna] = 1
                            mapeamento[8][0] = ultimaLinha
                            mapeamento[8][1] = ultimaColuna
                            return (linha, coluna)
    
                # percorro a linha da peca, da esquerda pra direita
                linha = ultimaLinha
                for a in range(-1, 2, 2):
                    coluna = ultimaColuna + a
                    if (coluna >= 0 and coluna <= 7 and tabuleiro[linha][coluna].estado == 0 and mapeamento[linha][coluna] == 0):
                        mapeamento[linha][coluna] = 1
                        mapeamento[8][0] = ultimaLinha
                        mapeamento[8][1] = ultimaColuna
                        return (linha, coluna)
                        
                (ultimaLinha, ultimaColuna) = self.proxPeca(ultimaLinha, ultimaColuna, tabuleiro, oponente)
        return (-1,-1)


    # Funcao que cria a arvore do alfa-beta prunning
    # tabuleiroMiniMax = Copia do tabuleiro
    # profundidade = profundidade maxima que a arvore ira atingir
    # donoNivel = "vez" da recursao (min = 0 ou max = 1)s
    # primeiraChamada = flag de primeira chamada (1 = primeira chamada; 0 = demais)
    # jogadorAtual = 1 se vermelho; 2 se preto
    # heuristica = heuristica que sera usada 
    # Retorna tupla: (valor da funcao de avaliacao, tabuleiro)
    def minimax(self, tabuleiroMiniMax, profundidade, donoNivel, primeiraChamada, jogadorAtual, heuristica, alpha, beta):
        #descobre o proximo jogador
        if (jogadorAtual == 1):
            proximoJogador = 2
        elif (jogadorAtual == 2):
            proximoJogador = 1
        
        
        if primeiraChamada:
            thisTab = tabuleiroMiniMax
        else:
            thisTab = None
        
        # Caso base, ja iterou em toda a profundidade, ou jogo acabou
        if ((profundidade == 0) or (self.isFimJogo(tabuleiroMiniMax, 0, jogadorAtual))):
            if donoNivel:
                return (heuristica.calcula(tabuleiroMiniMax, jogadorAtual), thisTab)
            else:
                return (heuristica.calcula(tabuleiroMiniMax, proximoJogador), thisTab)
               
        #heuristica de mapeamento para melhorar a performance da busca de jogadas validas
        mapeamento = []
        row = [0] * 8        
        for item in row:
            mapeamento.append(copy.deepcopy(row))
        mapeamento.append([0,0])
           
        maximo = [float("-inf"), None]
        minimo = [float("inf"), None]
        novoTab = copy.deepcopy(tabuleiroMiniMax)
        jogadaAtual = self.proximaJogada(novoTab, mapeamento, jogadorAtual)
        
        while (jogadaAtual != (-1,-1)):
            # Verifico se a posicao retornada por proxima jogada eh uma jogada valida)
            if(self.jogadaValida(jogadaAtual[0],jogadaAtual[1], novoTab, 0, jogadorAtual)):
                novoTab[jogadaAtual[0]][jogadaAtual[1]].estado = jogadorAtual
                atual = self.minimax(novoTab, profundidade - 1, not(donoNivel), 0, proximoJogador, heuristica, alpha, beta)
                
                if donoNivel:
                    if atual[0] > maximo[0]:
                        maximo[0] = atual[0]
                        if primeiraChamada:
                            maximo[1] = novoTab
                        else:
                            maximo[1] = None
                    if atual[0] > alpha:
                        alpha = atual[0]        
                    if alpha >= beta:
                        return (alpha,maximo[1])
                else:
                    if atual[0] < minimo[0]:
                        minimo[0] = atual[0]
                        if primeiraChamada:
                            minimo[1] = novoTab
                        else:
                            minimo[1] = None
                    if atual[0] < beta:
                        beta = atual[0]
                    if alpha >= beta:
                        return (beta,minimo[1]) 
                            
                #geramos um novo tabuleiro apenas se o atual foi modificado            
                novoTab = copy.deepcopy(tabuleiroMiniMax)                               
            jogadaAtual = self.proximaJogada(novoTab, mapeamento, jogadorAtual)
        
        # Nenhuma jogada para o jogador atual, passo a vez
        if (donoNivel and maximo[0] == float("-inf")) or ((not donoNivel) and minimo[0] == float("inf")):
            return self.minimax(tabuleiroMiniMax, profundidade - 1, not(donoNivel), 0, proximoJogador, heuristica, alpha, beta)
        
        if (donoNivel):
            return (maximo[0],maximo[1])
        else:
            return (minimo[0],minimo[1])
         
        
    def map(self, x, i):
        return int(round((x-self.offset[i])/41,0))


    def alternador(self):
        if self.last == 1:
            self.last = 2
            self.atual = 1
           # self.tempo = self.tempoVermelho
        else:
            self.last = 1
            self.atual = 2
            #self.tempo = self.tempoPreto
        return self.last