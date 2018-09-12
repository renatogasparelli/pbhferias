#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lib.util.datetime_util as dtutil
import lib.model.calendario as cal

from lib.model.periodoferiasbase import *
from lib.model.periodoferias import *



class JuncaoPeriodoFerias( AbsPeriodoFerias ):
    '''
    Representa a juncao de dois periodos de ferias
    '''
    def __init__(self, pfi, pff):
        
        if isinstance(pfi, FaltaFerias):
            AbsPeriodoFerias.__init__(self, pfi.N + pff.N, pff.foi, pff.fof, pfi.fri, pff.frf, pff.ecal)
        else:
            AbsPeriodoFerias.__init__(self, pfi.N + pff.N, pfi.foi, pfi.fof, pfi.fri, pff.frf, pff.ecal)
            
        self.pfi = pfi
        self.pff = pff
        self.__size = self._obter_size()
        self.__faltas = self._obter_faltas()
        self.__dias_faltosos = self.__obter_dias_faltosos()
            
    def printme(self):
        return '\n'.join(self._printme(0))

    def _printme(self, deep):
        y=[]
        y.append('\t'*deep + str(self))
        deep += 1
        for x in [self.pfi, self.pff]:
            if isinstance(x, JuncaoPeriodoFerias):
                y.extend(x._printme(deep))
            else:
                y.append('\t'*deep + x.printme())
        return y
 
    def reportme(self, details):
        return '\n'.join(self._reportme(details, 0))
    
    def _reportme(self, details, deep):
        y=[]
        y.append( AbsPeriodoFerias.reportme(self, False, deep))
        for x in [self.pfi, self.pff]:
            if isinstance(x, JuncaoPeriodoFerias):
                y.extend(x._reportme(details, deep + 1))
            else:
                y.append(x.reportme(details, deep + 1))
        return y

    def size(self):
        return self.__size
        
    def _obter_size( self ):
        n = 0
        for child in [ self.pfi, self.pff ]:
            if isinstance(child, JuncaoPeriodoFerias):
                n += child._obter_size()
            elif isinstance(child, FaltaFerias):
                pass
            elif isinstance(child, AbsPeriodoFerias):
                n += child.size()
            else:
                raise Exception('Tipo %s não esperado'%str(type(child)))
        return n

    #
    # quantidade de dias faltosos
    def faltas(self):
        return self.__faltas
    
    def _obter_faltas( self ):
        n = 0
        for child in [ self.pfi, self.pff ]:
            if isinstance(child, JuncaoPeriodoFerias):
                n += child._obter_faltas()
            elif isinstance(child, FaltaFerias):
                n += child.size()
            elif isinstance(child, AbsPeriodoFerias):
                pass
            else:
                raise Exception('Tipo %s não esperado'%str(type(child)))
        return n

    #
    # relação dos dias faltosos
    def dias_faltosos(self):
        return self.__dias_faltosos

    def __obter_dias_faltosos(self):
        n = []
        for child in [ self.pfi, self.pff ]:
            if isinstance(child, JuncaoPeriodoFerias):
                n += child.__obter_dias_faltosos()
            elif isinstance(child, FaltaFerias):
                for x in cal.CalFeriadosEFacultativos.dias_uteis(child.foi, child.fof):
                    n.append(x)
            elif isinstance(child, AbsPeriodoFerias):
                pass
            else:
                raise Exception('Tipo %s não esperado'%str(type(child)))
        return n

    #
    # retorna verdadeiro as todas as faltas ocorrerem
    #   no ano/mes de retorno oficial
    def faltas_apenas_no_retorno(self):
        dref = self.fof
        for df in self.dias_faltosos():
            if not ( df.year == dref.year and df.month == dref.month ):
                return False
        return True

class ComposicaoPeriodos:
    
    def __init__(self, pi, pf):
        self.pi = pi
        self.pf = pf


def concatena_periodos(pi, pf):
    '''
    
    A opção de férias final deve começar depois da opção de férias inicial, o limite acontece quando:
        1 - [ pi.fof < pf.foi ] e [ pi.frf >= pf.fri ]
           _______________________
         /     /           \      \
     pi.fri  pi.foi     pi.fof   pi.frf
                              _______________________
                            /      /         \       \
                        pf.fri  pf.foi     pf.fof   pf.frf
                            
        2 - (pi.fof == pi.frf) and ( pf.fof == pf.frf ) and ((pf.foi - pi.fof).days == 1) 
        
    '''
    
    if pi == None or pf == None:
        return None
    
    if pi.fof < pf.foi and pi.frf >= pf.fri:
        return ComposicaoPeriodos( pi, pf )
    
    if (pi.fof == pi.frf) and ( pf.fof == pf.frf ) and ((pf.foi - pi.fof).days == 1):
        return ComposicaoPeriodos( pi, pf )
    
    return None

    

    

