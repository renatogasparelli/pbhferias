#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gear
import codecs

from lib.model.periodoferiasbase import Config
from lib.model.calendario import CalendarioPbh

import lib.util.datetime_util as dtutil

Config.setMinInterval( 30 )
Config.setRegraTrimestreFeriasRegular( False )
Config.setRegraTrimestreLicencaAssiduidade( True )

Charset='utf8'

Anos =  [ 2019, 2020, 2021 ] 
Functions = [ gear.select3, gear.select2, gear.select1 ]


#
#
def main():   
    
    for ano in Anos:
    
        print 'Ano >> %d'%ano
    
        config = [
            (False, 'report_output/report_%d.txt'%ano ),
            (True , 'report_output/report_%d_detail.txt'%ano )
        ]
        
        for print_detail, report_name in config:
            
            Config.setReportDetail( print_detail )
            with codecs.open( report_name, 'w', Charset ) as fout:
                for i in report( ano ):
                    fout.write( str(i).decode( Charset ) )
                    fout.write('\n')


#
#
def report( ano, top=10 ):

    data = []
    #
    #
    data.append( '' )
    for i in gear.feriados(ano): data.append( i )
    data.append( '' )
    #
    #
    cnt = 1
    for fct in Functions:
        #
        planos = obter_planos( ano, fct )
        if len(planos) == 0:
            continue
        #
        oplanos = sorted( planos, key=lambda x: -x.dias_corridos_reais() )
        #
        limitMin = oplanos[0].dias_corridos_reais() - 1
        #
        lcnt = 0
        for plano in oplanos:
            
            if lcnt == top:
                break
            lcnt += 1
            
            data.append( '*'*80 )
            data.append( '(%03d): %02d dias corridos reais.'%( cnt, plano.dias_corridos_reais() ) ) 
            data.append( str( plano ) )
            data.append( '' )
            cnt += 1
            
    return data


#
# 
def obter_planos( ano, function ):
    config = { 'ano':ano, 'mindias':40, 'limit':1000 }
    planos = []
    #ofspremio = []
    ofspremio = [ x for x in gear.generate_premio_options( ano ) ]
    for pfr1, pfr2, pfr3 in function( ano=ano, mindias=40, limit=1000  ):
        bplan = gear.PlanoAnual(CalendarioPbh, ano)
        bplan.add_opcao( pfr1 )
        bplan.add_opcao( pfr2 )
        bplan.add_opcao( pfr3 )
        if not bplan.validate():
            continue
        for ofp in ofspremio:
            pAnual = gear.PlanoAnual(CalendarioPbh, ano)
            pAnual.add_opcao( pfr1 )
            pAnual.add_opcao( pfr2 )
            pAnual.add_opcao( pfr3 )
            pAnual.add_opcao( ofp )
            if not pAnual.validate():
                continue
            planos.append( pAnual )
    return planos


#
#
if __name__ == '__main__':
    main()
