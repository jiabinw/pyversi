#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class NumeroPeca:
  
    contador = 0
    
    # Entrada o tabuleiro e qual o eh o jogador atual
    def numeroPecaContador(self, tabuleiro, jogadorAtual):	
	
        for i in range(8):
            for j in range(8):
	      peca = tabuleiro[i][j]
	      if jogadorAtual == 1 :
		contador += contador	
		
         contador = contador*100/64       
             
	return contador
      
      
      
