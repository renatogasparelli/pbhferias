#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime as dtime
import lib.util.datetime_util as dtutil

'''
fonte: http://www.inf.ufrgs.br/~cabral/tabela_pascoa.html
'''


FeriadosDinamicos = dict()

FeriadosDinamicos[2012] = (date(2012,  4,  8), date(2012,  2, 21), date(2012,  6,  7))
FeriadosDinamicos[2013] = (date(2013,  3, 31), date(2013,  2, 12), date(2013,  5, 30))
FeriadosDinamicos[2014] = (date(2014,  4, 20), date(2014,  3,  4), date(2014,  6, 19))
FeriadosDinamicos[2015] = (date(2015,  4,  5), date(2015,  2, 17), date(2015,  6,  4))
FeriadosDinamicos[2016] = (date(2016,  3, 27), date(2016,  2,  9), date(2016,  5, 26))
FeriadosDinamicos[2017] = (date(2017,  4, 16), date(2017,  2, 28), date(2017,  6, 15))
FeriadosDinamicos[2018] = (date(2018,  4,  1), date(2018,  2, 13), date(2018,  5, 31))
FeriadosDinamicos[2019] = (date(2019,  4, 21), date(2019,  3,  5), date(2019,  6, 20))
FeriadosDinamicos[2020] = (date(2020,  4, 12), date(2020,  2, 25), date(2020,  6, 11))
FeriadosDinamicos[2021] = (date(2021,  4,  4), date(2021,  2, 16), date(2021,  6,  3))
FeriadosDinamicos[2022] = (date(2022,  4, 17), date(2022,  3,  1), date(2022,  6, 16))
FeriadosDinamicos[2023] = (date(2023,  4,  9), date(2023,  2, 21), date(2023,  6,  8))
FeriadosDinamicos[2024] = (date(2024,  3, 31), date(2024,  2, 13), date(2024,  5, 30))
FeriadosDinamicos[2025] = (date(2025,  4, 20), date(2025,  3,  4), date(2025,  6, 19))
FeriadosDinamicos[2026] = (date(2026,  4,  5), date(2026,  2, 17), date(2026,  6,  4))
FeriadosDinamicos[2027] = (date(2027,  3, 28), date(2027,  2,  9), date(2027,  5, 27))
FeriadosDinamicos[2028] = (date(2028,  4, 16), date(2028,  2, 29), date(2028,  6, 15))
FeriadosDinamicos[2029] = (date(2029,  4,  1), date(2029,  2, 13), date(2029,  5, 31))
FeriadosDinamicos[2030] = (date(2030,  4, 21), date(2030,  3,  5), date(2030,  6, 20))
FeriadosDinamicos[2031] = (date(2031,  4, 13), date(2031,  2, 25), date(2031,  6, 12))
FeriadosDinamicos[2032] = (date(2032,  3, 28), date(2032,  2, 10), date(2032,  5, 27))
FeriadosDinamicos[2033] = (date(2033,  4, 17), date(2033,  3,  1), date(2033,  6, 16))
FeriadosDinamicos[2034] = (date(2034,  4,  9), date(2034,  2, 21), date(2034,  6,  8))
FeriadosDinamicos[2035] = (date(2035,  3, 25), date(2035,  2,  6), date(2035,  5, 24))
FeriadosDinamicos[2036] = (date(2036,  4, 13), date(2036,  2, 26), date(2036,  6, 12))
FeriadosDinamicos[2037] = (date(2037,  4,  5), date(2037,  2, 17), date(2037,  6,  4))
FeriadosDinamicos[2038] = (date(2038,  4, 25), date(2038,  3,  9), date(2038,  6, 24))
FeriadosDinamicos[2039] = (date(2039,  4, 10), date(2039,  2, 22), date(2039,  6,  9))
FeriadosDinamicos[2040] = (date(2040,  4,  1), date(2040,  2, 14), date(2040,  5, 31))
FeriadosDinamicos[2041] = (date(2041,  4, 21), date(2041,  3,  5), date(2041,  6, 20))
FeriadosDinamicos[2042] = (date(2042,  4,  6), date(2042,  2, 18), date(2042,  6,  5))
FeriadosDinamicos[2043] = (date(2043,  3, 29), date(2043,  2, 10), date(2043,  5, 28))
FeriadosDinamicos[2044] = (date(2044,  4, 17), date(2044,  3,  1), date(2044,  6, 16))
FeriadosDinamicos[2045] = (date(2045,  4,  9), date(2045,  2, 21), date(2045,  6,  8))
FeriadosDinamicos[2046] = (date(2046,  3, 25), date(2046,  2,  6), date(2046,  5, 24))
FeriadosDinamicos[2047] = (date(2047,  4, 14), date(2047,  2, 26), date(2047,  6, 13))
FeriadosDinamicos[2048] = (date(2048,  4,  5), date(2048,  2, 18), date(2048,  6,  4))
FeriadosDinamicos[2049] = (date(2049,  4, 18), date(2049,  3,  2), date(2049,  6, 17))
FeriadosDinamicos[2050] = (date(2050,  4, 10), date(2050,  2, 22), date(2050,  6,  9))
FeriadosDinamicos[2051] = (date(2051,  4,  2), date(2051,  2, 14), date(2051,  6,  1))
FeriadosDinamicos[2052] = (date(2052,  4, 21), date(2052,  3,  5), date(2052,  6, 20))
FeriadosDinamicos[2053] = (date(2053,  4,  6), date(2053,  2, 18), date(2053,  6,  5))
FeriadosDinamicos[2054] = (date(2054,  3, 29), date(2054,  2, 10), date(2054,  5, 28))
FeriadosDinamicos[2055] = (date(2055,  4, 18), date(2055,  3,  2), date(2055,  6, 17))
FeriadosDinamicos[2056] = (date(2056,  4,  2), date(2056,  2, 15), date(2056,  6,  1))
FeriadosDinamicos[2057] = (date(2057,  4, 22), date(2057,  3,  6), date(2057,  6, 21))
FeriadosDinamicos[2058] = (date(2058,  4, 14), date(2058,  2, 26), date(2058,  6, 13))
FeriadosDinamicos[2059] = (date(2059,  3, 30), date(2059,  2, 11), date(2059,  5, 29))
FeriadosDinamicos[2060] = (date(2060,  4, 18), date(2060,  3,  2), date(2060,  6, 17))
FeriadosDinamicos[2061] = (date(2061,  4, 10), date(2061,  2, 22), date(2061,  6,  9))
FeriadosDinamicos[2062] = (date(2062,  3, 26), date(2062,  2,  7), date(2062,  5, 25))
FeriadosDinamicos[2063] = (date(2063,  4, 15), date(2063,  2, 27), date(2063,  6, 14))
FeriadosDinamicos[2064] = (date(2064,  4,  6), date(2064,  2, 19), date(2064,  6,  5))
FeriadosDinamicos[2065] = (date(2065,  3, 29), date(2065,  2, 10), date(2065,  5, 28))
FeriadosDinamicos[2066] = (date(2066,  4, 11), date(2066,  2, 23), date(2066,  6, 10))
FeriadosDinamicos[2067] = (date(2067,  4,  3), date(2067,  2, 15), date(2067,  6,  2))
FeriadosDinamicos[2068] = (date(2068,  4, 22), date(2068,  3,  6), date(2068,  6, 21))
FeriadosDinamicos[2069] = (date(2069,  4, 14), date(2069,  2, 26), date(2069,  6, 13))
FeriadosDinamicos[2070] = (date(2070,  3, 30), date(2070,  2, 11), date(2070,  5, 29))
FeriadosDinamicos[2071] = (date(2071,  4, 19), date(2071,  3,  3), date(2071,  6, 18))
FeriadosDinamicos[2072] = (date(2072,  4, 10), date(2072,  2, 23), date(2072,  6,  9))
FeriadosDinamicos[2073] = (date(2073,  3, 26), date(2073,  2,  7), date(2073,  5, 25))
FeriadosDinamicos[2074] = (date(2074,  4, 15), date(2074,  2, 27), date(2074,  6, 14))
FeriadosDinamicos[2075] = (date(2075,  4,  7), date(2075,  2, 19), date(2075,  6,  6))
FeriadosDinamicos[2076] = (date(2076,  4, 19), date(2076,  3,  3), date(2076,  6, 18))
FeriadosDinamicos[2077] = (date(2077,  4, 11), date(2077,  2, 23), date(2077,  6, 10))
FeriadosDinamicos[2078] = (date(2078,  4,  3), date(2078,  2, 15), date(2078,  6,  2))

def get_tuple(ano):
    if ano not in FeriadosDinamicos:
        return (None, None, None)
    return FeriadosDinamicos[ano]

def paixao_de_cristo(ano):
    return data_pascoa(ano) - ( 2 * dtutil.ONE_DAY )

def data_pascoa(ano):
    return get_tuple(ano)[0]

def data_carnaval(ano):
    return get_tuple(ano)[1]

def data_corpus_christi(ano):
    return get_tuple(ano)[2]


class Evento(object):
    def __init__(self, titulo, dia):
        self.titulo = titulo
        self.dia = dia
    def __str__(self):
        return '%s - %s - %s'%(self.dia, dtutil.obter_dia_semana_ptbr(self.dia), self.titulo)

def feriados_bh(ano):
    return [
        Evento( 'Confraternização Universal', date(ano, 1, 1)),
        Evento( 'Carnaval', data_carnaval(ano)),
        Evento( 'Paixão de Cristo', paixao_de_cristo(ano)),
        Evento( 'Tiradentes', date(ano, 4, 21)),
        Evento( 'Dia do Trabalho', date(ano, 5, 1)),
        Evento( 'Corpus Christi', data_corpus_christi(ano)),
        Evento( 'Assunção de Nossa Senhora', date(ano, 8, 15)),
        Evento( 'Independência do Brasil', date(ano, 9, 7)),
        Evento( 'Nossa Senhora Aparecida', date(ano, 10, 12)),
        Evento( 'Finados', date(ano, 11, 2)),
        Evento( 'Proclamação da República', date(ano, 11, 15)),
        Evento( 'Imaculada Conceição', date(ano, 12, 8)),
        Evento( 'Natal', date(ano, 12, 25))
    ]


def facultativos_comuns(ano):
    days=list()
    m=dict()
    fbh = feriados_bh(ano)
    for e in fbh: m[e.titulo]=e.dia
    days.append( Evento( 'Carnaval, quarta-feira de cinzas (*)', m['Carnaval'] + dtutil.ONE_DAY ))
    days.append( Evento( 'Natal, véspera (*)', m['Natal'] - dtutil.ONE_DAY ))
    days.append( Evento( 'Confraternização Universal, véspera (*)', date(ano, 12, 31)))
    days.append( Evento( 'Dia do Servidor Público (***)', date(ano, 10, 28)))
    days.append( Evento( 'Paixão de Cristo, vespera (*) - Nanan', m['Paixão de Cristo'] - dtutil.ONE_DAY ))
    return sorted(days, key = lambda x : x.dia)


def facultativos_desejados(ano):
    Terca=2
    Quinta=4
    days=list()
    fbh = feriados_bh(ano)
    faccomuns = set([ x.dia for x in facultativos_comuns(ano) ])
    for e in fbh:
        if e.dia.isoweekday() == Terca:
            v = Evento('%s - vespera (**)'%e.titulo, e.dia - dtutil.ONE_DAY )
            if e.dia.year == v.dia.year and v.dia not in faccomuns:
                days.append( v )
                
        elif e.dia.isoweekday() == Quinta:
            v = Evento('%s - seguida (**)'%e.titulo, e.dia + dtutil.ONE_DAY )
            if e.dia.year == v.dia.year and v.dia not in faccomuns:
                days.append( v )
                
    return sorted(days, key = lambda x : x.dia)


def facultativos(ano):
    return facultativos_comuns(ano) + facultativos_desejados(ano)

def calendario(ano):
    return feriados_bh(ano) + facultativos(ano)


def explicacao():
    str='''
      * facultativo comum
     ** facultativo desejado
    *** facultativo flutuante
    '''
    return str


FERIADOS = { evento.dia : evento
    for ano in FeriadosDinamicos.keys()
        for evento in feriados_bh(ano) 
}

FACULTATIVOS = {
    evento.dia : evento
    for ano in FeriadosDinamicos.keys()
        for evento in facultativos_desejados(ano) + facultativos_comuns(ano)
}


def eh_feriado(x):
    return x in FERIADOS


def eh_facultativo(x) :
    return x in FACULTATIVOS
    
def qual_evento(x):
    if eh_feriado(x): return FERIADOS[x]
    elif eh_facultativo(x): return FACULTATIVOS[x]
    return None
        
    
