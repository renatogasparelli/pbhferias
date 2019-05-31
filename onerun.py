#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gear
import codecs
import datetime

import lib.util.datetime_util as dutil
import lib.model.calendario as cal

#
#
def main():   
    
    calFerias = cal.CalFeriados
    
    #
    datas_licenca_maternidade=[]
    licenca_maternidade_inicio = datetime.date(2019, 6, 3)
    licenca_maternidade_fim = licenca_maternidade_inicio
    while True:
        datas_licenca_maternidade.append( dutil.formata_data_ptbr( licenca_maternidade_fim ) )
        if len(datas_licenca_maternidade) == 180: break
        licenca_maternidade_fim += dutil.ONE_DAY
        
    
    #
    datas_ferias_regulares = []
    data_inicio_ferias_regulares = calFerias.proximo_dia_util( licenca_maternidade_fim )
    data_fim_ferias_regulares = data_inicio_ferias_regulares
    while True:
        if calFerias.eh_dia_util( data_fim_ferias_regulares ):
            datas_ferias_regulares.append( dutil.formata_data_ptbr( data_fim_ferias_regulares ) )
        if len(datas_ferias_regulares) == 25: break
        data_fim_ferias_regulares  +=  dutil.ONE_DAY
        
        
    
    #
    datas_ferias_premio = []
    data_inicio_ferias_premio = calFerias.proximo_dia_util( data_fim_ferias_regulares )
    data_fim_ferias_premio = data_inicio_ferias_premio
    while True:
        datas_ferias_premio.append( dutil.formata_data_ptbr( data_fim_ferias_premio ) )
        if len(datas_ferias_premio) == 30: break
        data_fim_ferias_premio +=  dutil.ONE_DAY
    
    #
    retorno_ao_trabalho = calFerias.proximo_dia_util( data_fim_ferias_premio )

    dSize = 60

    print '-'*dSize
    print 'licenca_maternidade_inicio =', dutil.formata_data_ptbr( licenca_maternidade_inicio )
    print 'licenca_maternidade_fim =', dutil.formata_data_ptbr( licenca_maternidade_fim )
    print '\tdatas_licenca_maternidade[%d]'%len(datas_licenca_maternidade), datas_licenca_maternidade
    print '-'*dSize
    print '-'*dSize
    print 'data_ferias_regulares_inicio => ', dutil.formata_data_ptbr( data_inicio_ferias_regulares )
    print 'data_ferias_regulares_fim => ', dutil.formata_data_ptbr( data_fim_ferias_regulares )
    print '\tdatas_ferias_regulares[%d]'%len(datas_ferias_regulares), datas_ferias_regulares
    print '-'*dSize
    print '-'*dSize
    print 'data_ferias_premio_inicio => ', dutil.formata_data_ptbr( data_inicio_ferias_premio )
    print 'data_ferias_premio_fim => ', dutil.formata_data_ptbr( data_fim_ferias_premio )
    print '\tdatas_ferias_premio[%d]'%len(datas_ferias_premio), datas_ferias_premio
    print '-'*dSize
    print '-'*dSize 
    print 'retorno_ao_trabalho => ', dutil.formata_data_ptbr( retorno_ao_trabalho )
    print '-'*dSize
    

    
    
    
    
    


#
#
if __name__ == '__main__':
    main()

