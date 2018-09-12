#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lib.util.datetime_util as dtutil
import lib.util.feriados as fer
import lib.model.calendario as cal


class ConfigSet:
    def __init__(self):
        self.__reportDetail = False
        self.__minInterval = 30
        self.__regra_trimestre_ferias_regular = False
        self.__regra_trimestre_licenca_assiduidade = False
    
    def getReportDetail(self): return self.__reportDetail
    def setReportDetail(self, x): self.__reportDetail = x

    def getMinInterval(self): return self.__minInterval
    def setMinInterval(self, x): self.__minInterval = x

    def getRegraTrimestreFeriasRegular( self): return self.__regra_trimestre_ferias_regular
    def setRegraTrimestreFeriasRegular( self, x ): self.__regra_trimestre_ferias_regular = x
    
    def getRegraTrimestreLicencaAssiduidade( self ): return self.__regra_trimestre_licenca_assiduidade
    def setRegraTrimestreLicencaAssiduidade( self, x ): self.__regra_trimestre_licenca_assiduidade = x
    

Config = ConfigSet()

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
class AbsPeriodoFerias(object):
    '''
    PeriodoFerias ou periodo de ferias possui 4 datas
        foi => inicio oficial
        fof => final oficial
        fri => inicio real
        frf => final real
        
               _______________________
             /     /           \      \
            fri   foi          fof    frf
        
    '''
    
    #
    #
    def __init__(self, N, foi, fof, fri, frf, cal):
        self.N = N
        self.foi=foi
        self.fof=fof
        self.fri=fri
        self.frf=frf
        self.ecal=cal # calendarion efetivo
        #
        self.__dias_corridos_reais = (self.frf - self.fri).days + 1

    #
    #
    def size(self):
        return self.N

    #
    #
    def contem(self, x):
        return self.fri <= x <= self.fri

    #
    #
    def dias_corridos_oficiais(self):
        return (self.fof - self.foi).days + 1
    
    #
    #
    def dias_corridos_reais(self):
        #if self.__dias_corridos_reais == None:
        #    self.__dias_corridos_reais = (self.frf - self.fri).days + 1
        return self.__dias_corridos_reais

    #
    #
    def alavancagem(self):
        return self.dias_corridos_reais() / float( self.dias_corridos_esperados() )

    #
    #
    def dias_corridos_esperados(self):
        return self.size()
   
    #
    #
    def __str__(self):
        return self.reportme( Config.getReportDetail() )
    
    #
    #
    def reportme(self, details, deep=0):
        subreport = []
        self.__report_head(subreport, deep)
        if details:
            self.__report_detail(subreport, deep)
        return '\n'.join(subreport)
    
    #
    #
    def __report_head(self, subreport, deep):
        tab = '\t'*deep
        if deep > 0:
            subreport.append( '%s\t%s'%(tab, str(type(self)) ))
        subreport.append(
            '%s\t%02d dias tirados com %02d dias aproveitados e %02d dias esperados [alavancagem:%05.5f]' % (
                tab,
                self.size(),
                self.dias_corridos_reais(),
                self.dias_corridos_esperados(),
                self.alavancagem(),
            )
        )
        subreport.append('%s\t\tOficialmente: início  das férias %s'%(tab, dtutil.formata_data_ptbr(self.foi) ))
        subreport.append('%s\t\tOficialmente: termino das férias %s'%(tab, dtutil.formata_data_ptbr(self.fof) ))
        subreport.append('%s\t\tRealmente   : início  das férias %s'%(tab, dtutil.formata_data_ptbr(self.fri) ))
        subreport.append('%s\t\tRealmente   : termino das férias %s'%(tab, dtutil.formata_data_ptbr(self.frf) ))
    
    #
    #
    def __report_detail(self, subreport, deep):
        tab = '\t'*deep
        cnt = 1
        for x in dtutil.dias_entre_datas(self.fri, self.frf):
            
            obs = []
            
            eh_final_de_semana = dtutil.eh_final_de_semana(x)
            eh_feriado = fer.eh_feriado(x)
            eh_facultativo = fer.eh_facultativo(x)
            
            if eh_feriado or eh_facultativo:
                obs.append( fer.qual_evento(x).titulo )
            
            if eh_final_de_semana:
                obs.append( 'Final de semana' )
            
            
            if ( self.ecal == None or not ( eh_final_de_semana or eh_feriado ) ) and ( self.foi <= x <= self.fof ):
                obs.append( '%s %02d'% ( self.termo(), cnt) )
                cnt += 1
            
            subreport.append('%s\t\t\t%-5s,%s %s' % ( tab,
                dtutil.obter_dia_semana_ptbr(x),
                dtutil.formata_data_ptbr(x),
                ' - '.join( obs ) )
            )



# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
class PeriodoFeriasPremio( AbsPeriodoFerias ):
    def termo(self): return 'Contador faltas prêmio'

    




# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
class PeriodoFeriasRegulamentar( AbsPeriodoFerias ):
    def termo(self): return 'Contador férias'
    
    def dias_uteis_oficiais(self):
        return cal.CalFeriados.conta_dias_uteis(self.foi, self.fof)

    def dias_uteis_reais(self):
        return cal.CalFeriados.conta_dias_uteis(self.fri, self.frf)
    
    def printme(self):
        return '[%02d -> %02d]o:[%s, %s]{c:%s|u:%s}; r[%s, %s]{c:%s|u:%s} - %s'%( self.size(), self.dias_corridos_esperados(),
            self.foi, self.fof, self.dias_corridos_oficiais(), self.dias_uteis_oficiais(),
            self.fri, self.frf, self.dias_corridos_reais(), self.dias_uteis_reais(), type(self)
        )

    #
    #
    def dias_corridos_esperados(self):
        x = self.size()
        z = int( x / 5 )
        w = int( x % 5 )
        y = (z * 7) + 2 + w
        return y




# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
class FaltaFerias( PeriodoFeriasRegulamentar ):
    def termo(self): return 'Contador faltas'



def periodos_colidem(pf1, pf2):
    return not (
        ( pf1.fri < pf2.fri and  pf1.frf < pf2.fri)
        or
        ( pf2.fri < pf1.fri and  pf2.frf < pf1.fri)
    )
    
def distancia(pf1, pf2):
    return dtutil.total_dias_entre_datas( pf1.frf, pf2.frf )





'''
def ordena(*periodos):
    return sorted( periodos, key=lambda x:x.fri)

'''


