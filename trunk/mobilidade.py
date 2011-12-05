#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class Mobilidade: # Calcula quanto de Mobilidade o meu adversario tem. Quanto mais movimentos ele tem pior para mim (ou seja, maior valor retornado), o raciocinio analogo vale para o contrario disso.
  
    # Entrada o tabuleiro e qual o eh o jogador atual
    def calcula(self, tabuleiro, jogadorAtual):
        if(jogadorAtual == 1):
            jogador = 2
        else:
            jogador = 1
        
        avaliacao = 0
        for i in range(8):
            for j in range(8):
                if tabuleiro[i][j].estado == 0:
                    avaliacao += self.jogadaValida(i, j, tabuleiro, jogador, 1)
        
        normalizado = ((28 - avaliacao) / float(64)) * 100
        
        return normalizado
        

    def jogadaValida(self, i, j, tabuleiroFimJogo, jogador, verifica): #0:jogadaInvalida, 1:jogadaValida 
        todosVirar = []
        virar = []
        jogadaValida = 0
        # PERCORRENDO COLUNAS
        for a in range(7 - i): # Para direita
            col = i + a + 1
            peca = tabuleiroFimJogo[col][j]
            resposta = self.verificaJogada(peca, a, jogador)
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
            resposta = self.verificaJogada(peca, a, jogador)
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
            resposta = self.verificaJogada(peca, a, jogador)
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
            resposta = self.verificaJogada(peca, a, jogador)
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
                resposta = self.verificaJogada(peca, a, jogador)
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
                resposta = self.verificaJogada(peca, a, jogador)
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
                resposta = self.verificaJogada(peca, a, jogador)
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
            resposta = self.verificaJogada(peca, a, jogador)
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
            if self.last == 1:
                cor = 2
            else:
                cor = 1
            for t in todosVirar:
                for t0 in t:
                    t0.estado = cor
        elif((jogadaValida != 1) and (not(verifica))):
            print "Erro: Jogada Invalida"           
                
        return jogadaValida


    def verificaJogada(self, peca, a, jogador): # 1:jogadaValida, 0:continua, 2:para
        if peca.estado == 0:
            return 2

        # Se a peca que esta percorrendo e a mesma do jogador atual e ha pelo menos uma peca entre as duas
        if peca.estado == jogador:
            if a > 0:
                return 1
            else:
                return 2

        return 0
