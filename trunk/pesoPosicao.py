#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *

class PesoPosicao: #Calcula quantos de pontos o jogadorAtual tem para estes pesos de tabuleiro
  
    # Entrada o tabuleiro e qual o eh o jogador atual
    def calcula(self, tabuleiro, jogadorAtual):    
    
        pesoPosicao = (
                        (120, -20, 20,  5,  5, 20,-20,120),
                        (-20, -40, -5, -5, -5, -5,-40,-20),
                        ( 20,  -5, 15,  3,  3, 15, -5, 20),
                        (  5,  -5,  3,  3,  3,  3, -5,  5),
                        (  5,  -5,  3,  3,  3,  3, -5,  5),
                        ( 20,  -5, 15,  3,  3, 15, -5, 20),
                        (-20, -40, -5, -5, -5, -5,-40,-20),
                        (120, -20, 20,  5,  5, 20,-20,120)
                      )
        maxAvaliacao = avaliacao = 0
        for i in range(8):
            for j in range(8):
                maxAvaliacao += pesoPosicao[i][j]
                if jogadorAtual == tabuleiro[i][j].estado:
                    avaliacao += pesoPosicao[i][j]

        normalizado = (avaliacao / float(maxAvaliacao)) * 100
        
        return normalizado