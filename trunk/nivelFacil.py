#!/usr/bin/env python
import os, sys, copy
from peca import *
from tabuleiro import *
from pesoPosicao import *
from numeroPeca import *
from mobilidade import *
from captura import *
from faseDoJogo import *

class NivelFacil:   
    
    # Calcula as heuristicas para o nivel facil, com peso para cada uma
    def calcula(self, tabuleiro, jogadorAtual):   
        valorPosicao = valorCaptura = valorMobilidade = valorNrPecas = 0
        
        pesoPosicao = pesoMobilidade = 0
        
        pesoCaptura = 1
        pesoNrPecas = 1
        
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