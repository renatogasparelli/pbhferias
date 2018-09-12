#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime
import calendar

DateFmt = '%d-%m-%Y'

ONE_DAY = timedelta(days=1)
TODAY = datetime.now()
THIS_YEAR = TODAY.year

DIAS_DA_SEMANA = [ 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo' ]

MESES_DO_ANO = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]


def dias_do_ano(ano):
    pdia = date(ano, 1, 1)
    udia = date(ano, 12, 31)
    for d in dias_entre_datas(pdia, udia):
        yield d


def dias_entre_datas(pdia, udia):
    cdia = pdia
    while cdia <= udia:
        yield cdia
        cdia += ONE_DAY


def total_dias_entre_datas(dt1, dt2):
    dtdiff = dt1 - dt2
    return abs( dtdiff.days )

def menor_data(*dts):
    return sorted(dts)[0]
    

def eh_final_de_semana(dia):
    return not ( 1 <= dia.isoweekday() <= 5 )


def obter_dia_semana_ptbr(dia):
    return DIAS_DA_SEMANA[ dia.isoweekday() - 1 ]


def formata_data_ptbr(dia):
    return '%(day)s de %(month)s de %(year)s'%{
        'year':dia.year,
        'month':MESES_DO_ANO[dia.month-1],
        'day':dia.day
    }


def dias_futuros(dia, span=None):
    
    def loop():
        if span == None:
            while True: yield
        else:
            for i in range(span): yield
                
    while loop():
        dia += ONE_DAY
        yield dia
            

def dias_passados(dia, span=None):
    
    def loop():
        if span == None:
            while True: yield
        else:
            for i in range(span): yield
    
    while loop():
        dia -= ONE_DAY
        yield dia

    
def limites_do_mes(ano, mes):
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return ( date(ano, mes, 1), date(ano, mes, ultimo_dia) )


def trimestres(ano):
    tpls = []
    spans = [ (1, 3), (4, 6), (7, 9), (10, 12) ]
    idx = 1
    for span in spans:
        n = calendar.monthrange(ano, span[1])[1]
        d1 = date(ano, span[0], 1)
        dn = date(ano, span[1], n)
        tpl = ( idx, d1, dn, total_dias_entre_datas(d1, dn) )
        tpls.append( tpl )
        idx+=1
    return tpls
    
    

