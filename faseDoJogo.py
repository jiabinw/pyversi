#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class FaseDoJogo:   
    
    # Retorna o valor normalizado do estado em que o jogo esta 
    # A funcao conta o numero de pecas do tabuleiro e normaliza o valor, retornando-o
    def estadoJogo(self, tabuleiro):
        
        contador = 0        
        for i in range(8):
            for j in range(8):
                peca = tabuleiro[i][j]
                if peca.estado != 0:
                    contador += 1   
                
        contador = (contador / float(64)) * 100             
        return contador