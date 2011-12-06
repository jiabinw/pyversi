#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class NumeroPeca:   
    
    # Entrada o tabuleiro e qual o eh o jogador atual
    def calcula(self, tabuleiro, jogadorAtual):
        if(jogadorAtual == 1):
            jogador = 2
        else:
            jogador = 1
            
        contadorMeu = 0        
        for i in range(8):
            for j in range(8):
                peca = tabuleiro[i][j]
                if peca.estado == jogadorAtual:
                    contadorMeu += 1   
        
        contador = 0        
        for i in range(8):
            for j in range(8):
                peca = tabuleiro[i][j]
                if peca.estado == jogador:
                    contador += 1   
        
        contador = ((contadorMeu - contador) / float(64)) * 100             
        return contador