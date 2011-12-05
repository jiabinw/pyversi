#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *
from pesoPosicao import *
from numeroPeca import *
from mobilidade import *
from captura import *
from faseDoJogo import *

class NivelDificil:   
    
    # Calcula as heuristicas para o nivel facil, com peso para cada uma
    def calcula(self, tabuleiro, jogadorAtual):
        faseJogo = FaseDoJogo().estadoJogo(tabuleiro) # Retorna quantos porcento de jogo ja aconteceu.        
        
        pesoPosicao = pesoCaptura = pesoMobilidade = pesoNrPecas = valorPosicao = valorCaptura = valorMobilidade = valorNrPecas = 0
        
        if faseJogo < 20:
            pesoPosicao = 2
            pesoMobilidade = 1
        elif faseJogo >= 20 and faseJogo < 45:
            pesoPosicao = 2
            #pesoCaptura = 2
            pesoMobilidade = 4
            #pesoNrPecas = 1
        elif faseJogo >= 45 and faseJogo < 65:
            pesoPosicao = 4
            #pesoCaptura = 2
            pesoMobilidade = 2
            pesoNrPecas = 1
        elif faseJogo >= 65 and faseJogo < 85:
            pesoPosicao = 4
            pesoMobilidade = 3
            pesoCaptura = 2
            pesoNrPecas = 3.5
        else: # TODO fazer forca-bruta em cima do numero de pecas. A partir do nivel maximo que o alpha beta prunning eh aconselhavel
            pesoPosicao = 2
            pesoCaptura = 1.5
            pesoNrPecas = 2.75
        
        if(pesoPosicao > 0):
            valorPosicao = PesoPosicao().calcula(tabuleiro, jogadorAtual)
            valorPosicao *= pesoPosicao
            
        if(pesoMobilidade > 0):
            valorMobilidade = Mobilidade().calcula(tabuleiro, jogadorAtual)
            valorMobilidade *= pesoMobilidade
            
        if(pesoCaptura > 0):
            valorCaptura = Captura().calcula(tabuleiro, jogadorAtual)
            valorCaptura *= pesoCaptura
            
        if(pesoNrPecas > 0):
            valorNrPecas = NumeroPeca().calcula(tabuleiro, jogadorAtual)
            valorNrPecas *= pesoNrPecas            
            
        valorFinal = (valorCaptura + valorMobilidade + valorNrPecas + valorPosicao) / (pesoPosicao + pesoMobilidade + pesoCaptura + pesoNrPecas)
        
        return valorFinal      