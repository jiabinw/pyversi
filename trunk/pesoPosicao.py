#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class PesoPosicao: #Calcula quantos de pontos o jogadorAtual tem para estes pesos de tabuleiro
  
    # Entrada o tabuleiro e qual o eh o jogador atual
    def calcula(self, tabuleiro, jogadorAtual):    
        if(jogadorAtual == 1):
            jogador = 2
        else:
            jogador = 1
            
        pesoPosicao = (
                        (1200, -40, 20, 10, 10, 20, -40,1200),
                        (-40,-120, 10,-10,-10, 10,-120,-40),
                        ( 20,  10, 15,  3,  3, 15,  10, 20),
                        ( 10, -10,  3,  3,  3,  3, -10, 10),
                        ( 10, -10,  3,  3,  3,  3, -10, 10),
                        ( 20,  10, 15,  3,  3, 15,  10, 20),
                        (-40,-120, 10,-10,-10, 10,-120,-40),
                        (1200, -40, 20, 10, 10, 20, -40,1200)
                      )
        minhaAvaliacao = avaliacao = 0
        for i in range(8):
            for j in range(8):
                if jogador == tabuleiro[i][j].estado:
                    avaliacao += pesoPosicao[i][j]
                    
        for i in range(8):
            for j in range(8):
                if jogadorAtual == tabuleiro[i][j].estado:
                    minhaAvaliacao += pesoPosicao[i][j]

        normalizado = ((minhaAvaliacao - avaliacao) / float(64)) * 100
        
        #print "normalizado", normalizado
        
        return normalizado