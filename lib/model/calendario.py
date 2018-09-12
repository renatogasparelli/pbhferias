#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lib.util.datetime_util as dtutil
import lib.util.feriados as fer

class Calendario:
    
    def __init__(self, datas_especiais):
        self.datas_especiais = datas_especiais
    
    def eh_final_de_semana(self, x): return dtutil.eh_final_de_semana( x )
    def eh_data_especial(self, x): return x in self.datas_especiais
    def eh_dia_util(self, x): return not ( self.eh_final_de_semana(x) or self.eh_data_especial(x) )
    def obter_evento(self, x): return self.datas_especiais[x]
        
    def dias_do_ano(self, ano):
        for x in  dtutil.dias_do_ano( ano ):
            yield x
    
    def proximo_dia_util(self, x):
        for y in dtutil.dias_futuros(x):
            if self.eh_dia_util(y):
                return y
    
    def previo_dia_util(self, x):
        for y in dtutil.dias_passados(x):
            if self.eh_dia_util(y):
                return y
    
    def dias_uteis(self, x1, x2):
        for x in dtutil.dias_entre_datas(x1, x2):
            if self.eh_dia_util(x):
                yield x
    
    def conta_dias_uteis(self, x1, x2):
        y = 0
        for x in self.dias_uteis(x1, x2):
            y += 1
        return y
    

# ----------------------------------------------------------------------------
# As datas especiais são os feriados
# ----------------------------------------------------------------------------
DatasCalFeriados = {}
DatasCalFeriados.update( fer.FERIADOS )
CalFeriados = Calendario( DatasCalFeriados )

# ----------------------------------------------------------------------------
# As datas especiais são os feriados e pontos facultativo
# ----------------------------------------------------------------------------#
DatasCalFeriadosEFacultativos = {}
DatasCalFeriadosEFacultativos.update( fer.FERIADOS )
DatasCalFeriadosEFacultativos.update( fer.FACULTATIVOS )
CalFeriadosEFacultativos = Calendario( DatasCalFeriadosEFacultativos )

CalendarioPbh = CalFeriadosEFacultativos

# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
CalSimples = Calendario( {} )


