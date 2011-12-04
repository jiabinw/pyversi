#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class NumeroPeca:
  
    maxPontuacao = 0
    melhorJogada = [0,0]
  
    # Entrada o tabuleiro e qual o eh o jogador atual
    def __init__(self, tabuleiro, jogadorAtual):	
	
        for i in range(8):
            for j in range(8):
	      novoTab = copy.deepcopy(tabuleiro)
	      peca = novoTab[i][j]	      
	      novoTab.jogadaValida(i, j, novoTab, 0)
	      novoTab.pontuacao
	      
	      if jogadorAtual == 1 :
		if novoTab.pontosVermelho > maxPontuacao:
		  maxPontuacao = novoTab.pontosVermelho
		  melhorJogada = [i,j]
	      else
		if novoTab.pontosPreto > maxPontuacao:
		  maxPontuacao = novoTab.pontosPreto
		  melhorJogada = [i,j]
		
                
             
	return melhorJogada
      
      
      
