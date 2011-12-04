#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class Captura:
  
    novoTab = []
      
    def calcula(self, tabuleiro, jogadorProx):	     
      
      if len(self.novoTab) == 0: #inicializa
	row = [0]*8        
	for item in row:
	  self.novoTab.append(copy.deepcopy(row))
      else:  #somente atualiza
	for i in range(8):
	  for j in range(8):            
	    self.novoTab[i][j] = 0
	  
      contador = 0
      contadorAtual = 0
     
      for i in range(8):
	for j in range(8):
	  if tabuleiro[i][j].estado == 0:
	   self.jogadaValida(i, j, tabuleiro, 0, jogadorProx)
	  
      for i in range(8):
	for j in range(8):
	  contador = contador + self.novoTab[i][j]
     
      if jogadorProx == 1:
	jogadorAtual = 2
      else:
	jogadorAtual = 1
     
      for i in range(8):
	for j in range(8):
	  if tabuleiro[i][j].estado == jogadorAtual:
	    contadorAtual += 1
     
      captura = contadorAtual - contador
      
      captura / float(contadorAtual) * 100
		  
      return captura
	  
	  
	  

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
                virar.append([col,j])

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
                virar.append([col,j])
        
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
                virar.append([i,lin])

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
                virar.append([i,lin])

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
                    virar.append([col,lin])
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
                    virar.append([col,lin])
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
                    virar.append([col,lin])
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
                virar.append([col,lin])


        # Se a jogada for valida, da o flip nas pecas para a cor do jogador corrente
        if ((jogadaValida == 1) and (not(verifica))):
            for t in todosVirar:
                for t0 in t:
                    col,lin = t0
                    self.novoTab[col][lin] = 1
                    
       
                
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