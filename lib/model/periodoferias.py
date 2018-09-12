#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lib.util.datetime_util as dtutil
import lib.util.feriados as fer
import lib.model.calendario as cal

from lib.model.periodoferiasbase import *


#
#
def __new_periodo_ferias(x, N, Calendario=None):
    #
    # um periodo sem dias não importa
    if N == 0:
        return None
    
    '''
    modelo específico para o caso pbh - conatgem de N dias úteis
    
    sejam:
      x <- data arbitraria
      N <- dias úteis das férias
      dias_nao_uteis_1 <- feriados + pontos facultativos admitidos
      dias_nao_uteis_2 <- feriados
   
    data_oficial_inicio_ferias [doif] - início do período marcado na folha
    data_oficial_fim_ferias [doff] - final do período marcado na folha
    data_real_inicio_ferias [drif] - início do período corrente (real) de férias
    data_real_fim_ferias [drff] - final do período corrente (real) de férias
    '''
    #dias_nao_uteis_1 = FERIADOS_OU_FACULTATIVOS
    #dias_nao_uteis_2 = FERIADOS
    
    #
    # (1) definir doif com um dia útil arbitrário
    #   férias são contabilizados sobre dias úteis, logo dia não útil não serve
    #   para fins de data oficial
    if not cal.CalFeriadosEFacultativos.eh_dia_util(x):
        return None
    data_oficial_inicio_ferias = x

    #
    # (2) definir doff como o N'esino dia útil(**) à partir doif (incluindo doif)
    #   é importante observar que ponto facultativo para fins de férias é dia útil
    #
    #   obs: os dias oficiais precisam ser N dias corridos
    data_oficial_fim_ferias = data_oficial_inicio_ferias
    i = 1
    while i < N:
        data_oficial_fim_ferias += dtutil.ONE_DAY
        if Calendario == None:
            i += 1
        elif Calendario.eh_dia_util(data_oficial_fim_ferias):
            i += 1

    #
    # (3) definir drif como o dia imediatamente posterior ao primeiro
    #   dia útil antes de doif (não incluindo doif)
    data_real_inicio_ferias = cal.CalFeriadosEFacultativos.\
            previo_dia_util( data_oficial_inicio_ferias ) + dtutil.ONE_DAY

    #
    # (4) definir drff como o dia imediatamente anterior ao próximo 
    #   dia útil após de doff (não incluíndo doff)
    data_real_fim_ferias = cal.CalFeriadosEFacultativos.\
            proximo_dia_util( data_oficial_fim_ferias ) - dtutil.ONE_DAY
    
    
    return ( N,
        data_oficial_inicio_ferias,
        data_oficial_fim_ferias,
        data_real_inicio_ferias,
        data_real_fim_ferias,
        Calendario
    )

#
#
def new_periodo_ferias(x, N):
    t = __new_periodo_ferias( x, N, cal.CalFeriados )
    if t == None:
        return None
    return PeriodoFeriasRegulamentar( *t )

#
#
def new_periodo_faltas(x, N):
    t = __new_periodo_ferias( x, N, cal.CalFeriadosEFacultativos )
    if t == None:
        return None
    return FaltaFerias( *t )

#
#
def new_periodo_ferias_premio(x, N):
    t = __new_periodo_ferias( x, N )
    if t == None:
        return None
    return PeriodoFeriasPremio( *t )













# 