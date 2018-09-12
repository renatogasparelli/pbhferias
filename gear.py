#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import itertools

import lib.util.datetime_util as dtutil
import lib.util.dbclient as db
import lib.model.periodoferias as mpf
import lib.model.composicaoperiodos as cp
import lib.model.calendario as cal
import lib.util.feriados as fer

from lib.model.periodoferiasbase import *

FOR_REAL=False
VERBOSE=False


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------    
def anos( fAno=2079 ):
    # 2012 -> 2079
    for ano in range(2012, fAno):
        yield ano




# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------    
def feriados(ano):
    for i in sorted( fer.calendario( ano ), key = lambda x : x.dia ):
        yield i
    yield fer.explicacao()




# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def periodos_colidem(pf1, pf2):
    return not (
        ( pf1.fri < pf2.fri and  pf1.frf < pf2.fri)
        or
        ( pf2.fri < pf1.fri and  pf2.frf < pf1.fri)
    )



# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def generate_feriadao_options( ano ):
    pass


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def generate_premio_options( ano ):
    
    #print 'processando ano %d'%ano
    for dia in dtutil.dias_do_ano(ano):
    
        
        #
        #   As ferias devem começar em dia útil.
        # não serve final de semana, feriado ou ponto facultativo
        if not cal.CalFeriadosEFacultativos.eh_dia_util( dia ):
            if VERBOSE:
                print '\tFérias devem começar em dia de trabalho!'
            continue
        
        #
        # tamanho das ferias
        for N in [ 30 ]:

            if N == 0:
                if VERBOSE:
                    print '\tFérias de 0 dias é apenas figurativo.'
                continue
    
            #
            #   Gera a opção de ferias para a data e span informados
            pf = mpf.new_periodo_ferias_premio(dia, N)

            #
            #   As férias não podem ter menos de 10 dias corridos
            if pf.dias_corridos_oficiais() < 10:
                if VERBOSE:
                    print 'As férias devem ter pelo menos 10 dias corridos.'
                continue
            
            yield pf







# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def generate_regular_options( ano ):
    
    
    #print 'processando ano %d'%ano
    for dia in dtutil.dias_do_ano(ano):
        

        #
        #   As ferias devem começar em dia útil.
        # não serve final de semana, feriado ou ponto facultativo
        if not cal.CalFeriadosEFacultativos.eh_dia_util( dia ):
            if VERBOSE:
                print '\tFérias devem começar em dia de trabalho!'
            continue
        
        #
        # tamanho das ferias
        for N in range(1, 26):

            if N == 0:
                if VERBOSE:
                    print '\tFérias de 0 dias é apenas figurativo.'
                continue
    
            #
            #   Gera a opção de ferias para a data e span informados
            pf = mpf.new_periodo_ferias(dia, N)

            #
            #   As férias não podem ter menos de 10 dias corridos
            if pf.dias_corridos_oficiais() < 10:
                if VERBOSE:
                    print 'As férias devem ter pelo menos 10 dias corridos.'
                continue
            
            yield pf




# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def gerador_opcoes_com_falha( pfref, faltas):
    
    #print pfref
    
    for fd in range(faltas + 1):
        
        fe = faltas - fd
        
        #print fe, fd
        
        pfs = []
        
        if fe > 0:
            x = pfref.fri - fe * dtutil.ONE_DAY
            pfe = mpf.new_periodo_faltas( x, fe )
            if pfe != None: pfs.append( pfe )
        
        pfs.append( pfref )
        
        if fd > 0:
            x = pfref.frf + dtutil.ONE_DAY
            pfd = mpf.new_periodo_faltas( x, fd )
            if pfd != None: pfs.append( pfd ) 
        
        if not cp.eh_admissivel_concatenar( pfs ):
            continue
            
        pfc = cp.ComposicaoPeriodos( pfs )
        if not cp.falta_coberto( pfc ):
            continue
        
        yield pfc
               



# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

def select1( **config ): return __select( 'sqls/opcoes_de_ferias_1_periodos.sql', **config )
def select2( **config ): return __select( 'sqls/opcoes_de_ferias_2_periodos.sql', **config )
def select3( **config ): return __select( 'sqls/opcoes_de_ferias_3_periodos.sql', **config )

def __select( query, **config ):
    def read_config(x, dft=None):
        if x not in config:
            return dft
        return config[x]
    
    ano=read_config('ano')
    mindias=read_config('mindias')
    limit=read_config('limit', 50)
    
    with codecs.open( query , 'r', 'utf8') as fin:
        sql = fin.read()
    
    sql = sql.replace(':ano:', str(ano).encode('utf8') )\
        .replace(':minimo_dias_corridos_reais:', str(mindias).encode('utf8') )\
        .replace(':limit:', str(limit).encode('utf8') )
    
    # print sql
    
    db.PessoalLocal.connect()
    result = db.PessoalLocal.select( sql )
    db.PessoalLocal.close()
    
    lineMask = LineMask()
    for i in result:
        lineMask.setLine(i)
        
        pfr1 = mpf.PeriodoFeriasRegulamentar( lineMask.p1_tamanho
            , lineMask.p1_inicio_oficial, lineMask.p1_fim_oficial
            , lineMask.p1_inicio_real, lineMask.p1_fim_real, cal.CalFeriados )
        
        pfr2 = None
        if lineMask.p2_tamanho != None:
            pfr2 = mpf.PeriodoFeriasRegulamentar( lineMask.p2_tamanho
                , lineMask.p2_inicio_oficial, lineMask.p2_fim_oficial
                , lineMask.p2_inicio_real, lineMask.p2_fim_real, cal.CalFeriados )
        
        pfr3 = None
        if lineMask.p3_tamanho != None:
            pfr3 = mpf.PeriodoFeriasRegulamentar( lineMask.p3_tamanho
                , lineMask.p3_inicio_oficial, lineMask.p3_fim_oficial
                , lineMask.p3_inicio_real, lineMask.p3_fim_real, cal.CalFeriados )
        
        yield pfr1, pfr2, pfr3


            
# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------            
class PlanoAnual:
    
    def __init__(self, calendario, ano):
        self.calendario = calendario
        self.ano = ano
        self.__folgas = []
        self.__ferias_premio_idx = None


    def add_opcao(self, x):
        if x == None:
            return
        if isinstance( x, mpf.PeriodoFeriasPremio ):
            self.__ferias_premio_idx = len( self.__folgas )
        self.__folgas.append( x )
        
    def validate(self):
        
        #
        # verifica se os intervalos colidem, o que torna a alternativa invalida
        for fi, fj in itertools.product( self.__folgas, self.__folgas ):
            if fi == fj:
                continue
            if periodos_colidem( fi, fj ):
                return False
        
        #
        # verifica o intervalo minimo de dias entre ferias
        self.__folgas = sorted(self.__folgas, key=lambda x : x.fri )
        idx = 1
        for i in range(0, len(self.__folgas)-1):
            if dtutil.total_dias_entre_datas( self.__folgas[i].frf, self.__folgas[i+1].fri) <= Config.getMinInterval():
                return False
        
        #
        # eh preciso que se trabalhe ao menos 60 dias no trimestre
        #if self.__ferias_premio_idx != None:
        #    
            
        for k in range(len(self.__folgas)):
            
            if k == self.__ferias_premio_idx:
                if not Config.getRegraTrimestreLicencaAssiduidade():
                    continue
            else:
                if not Config.getRegraTrimestreFeriasRegular():
                    continue
            
            ferK = self.__folgas[k]
            dias = [ 0, 0, 0, 0 ]
            for idx, d1, dn, n in dtutil.trimestres( self.ano ):
                nidx = idx - 1
                dias[ nidx ] = n
                
                if d1 <= ferK.foi <= dn and d1 <= ferK.fof <= dn :
                    dias[ nidx ] -= ( ferK.N )
                    break
                
                elif d1 <= ferK.foi <= dn:
                    dias[ nidx ] -= ( dtutil.total_dias_entre_datas( ferK.foi, dn ) )

                elif d1 <= ferK.fof <= dn:
                    dias[ nidx ] -= ( dtutil.total_dias_entre_datas( d1, ferK.fof ) )
            
            for d in dias:
                if d <= 60:
                    return False
        
        
        #
        # se nao houve motivo de invalidacao, admite-se validado
        return True

    def okey1(self):
        mindias = self.dias_corridos_reais()
        cnt_dias_trabalho, cnt_dias_folgado = self.cnt_dias()
        return mindias * 1000 + cnt_dias_folgado

    def okey2(self):
        mindias = self.dias_corridos_reais()
        cnt_dias_trabalho, cnt_dias_folgado = self.cnt_dias()
        return cnt_dias_folgado * 100 + mindias

    def cnt_dias(self):
        cnt_dias_trabalho = 0
        cnt_dias_folgado = 0        
        for x in self.calendario.dias_do_ano( self.ano ):
            if self.__eh_dia_trabalho(x):
                cnt_dias_trabalho += 1
            else:
                cnt_dias_folgado += 1
        return ( cnt_dias_trabalho, cnt_dias_folgado )
    
    
    def dias_corridos_reais(self):
        acm = 0
        for x in self.__folgas:
            acm += x.dias_corridos_reais()
        return acm
    
    def __str__(self):
        buf = []
        for folga in sorted(self.__folgas, key=lambda x : x.fri ):
            buf.append( str( folga ) )
        return '\n'.join(buf)


    def __eh_dia_trabalho(self, x):
        #
        # se for dia util no calendário, então eh a princípio
        # dia util
        if self.calendario.eh_dia_util( x ):
            #
            # exceto se for dia de folga, que inclui férias e fugas
            for folga in self.__folgas:
                if folga.contem( x ):
                    return False
            #
            return True
        #
        return False



# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
class LineMask:
    
    def __basicSet(self, line):
        size = len(line)
        self.__line = line
        self.__line_maxidx = size - 3
        self.soma = line[size - 2]
        self.esperados = line[size - 1]
    
    def setLine(self, line):
        self.__basicSet( line )
        
        sline = self.__readLine( 0 )
        self.p1_inicio_real = sline[0]
        self.p1_inicio_oficial = sline[1]
        self.p1_fim_oficial = sline[2]
        self.p1_fim_real = sline[3]
        self.p1_tamanho = sline[4]
        self.p1_aproveitados = sline[5]
        sline = None
        
        sline = self.__readLine( 6 )
        self.p2_inicio_real = sline[0]
        self.p2_inicio_oficial = sline[1]
        self.p2_fim_oficial = sline[2]
        self.p2_fim_real = sline[3]
        self.p2_tamanho = sline[4]
        self.p2_aproveitados = sline[5]
        sline = None
        
        sline = self.__readLine( 12 )
        self.p3_inicio_real = sline[0]
        self.p3_inicio_oficial = sline[1]
        self.p3_fim_oficial = sline[2]
        self.p3_fim_real = sline[3]
        self.p3_tamanho = sline[4]
        self.p3_aproveitados = sline[5]
        sline = None
        
    
    def __readLine(self, shift):
        if self.__line_maxidx >= shift:
            return ( self.__line[ shift     ], self.__line[ shift + 1 ],
                     self.__line[ shift + 2 ], self.__line[ shift + 3 ],
                     self.__line[ shift + 4 ], self.__line[ shift + 5 ] )
        return (None, None, None, None, None, None)





















# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------    
