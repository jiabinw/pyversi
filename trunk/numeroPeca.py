#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class NumeroPeca:
  
    contador = 0
    
    # Entrada o tabuleiro e qual o eh o jogador atual
    def calcula(self, tabuleiro, jogadorAtual):	
	
        for i in range(8):
            for j in range(8):
	      peca = tabuleiro[i][j]
	      if peca.estado == jogadorAtual :
		contador += contador	
		
         contador = contador*100/64       
             
	return contador
      
      
      
