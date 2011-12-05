#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class PesoPosicao: #Calcula quantos de pontos o jogadorAtual tem para estes pesos de tabuleiro
  
    # Entrada o tabuleiro e qual o eh o jogador atual
    def calcula(self, tabuleiro, jogadorAtual):    
    
        pesoPosicao = (
                        (120, -40, 20, 10, 10, 20, -40,120),
                        (-40,-120, 10,-10,-10, 10,-120,-40),
                        ( 20,  10, 15,  3,  3, 15,  10, 20),
                        ( 10, -10,  3,  3,  3,  3, -10, 10),
                        ( 10, -10,  3,  3,  3,  3, -10, 10),
                        ( 20,  10, 15,  3,  3, 15,  10, 20),
                        (-40,-120, 10,-10,-10, 10,-120,-40),
                        (120, -40, 20, 10, 10, 20, -40,120)
                      )
        maxAvaliacao = avaliacao = 0
        for i in range(8):
            for j in range(8):
                maxAvaliacao += pesoPosicao[i][j]
                #print "i", i, "j", j, " peso", pesoPosicao[i][j]
                if jogadorAtual == tabuleiro[i][j].estado:
                    avaliacao += pesoPosicao[i][j]

        normalizado = (avaliacao / float(64)) * 100
        
        #print "normalizado", normalizado
        
        return normalizado