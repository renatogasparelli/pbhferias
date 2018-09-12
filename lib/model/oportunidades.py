#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lib.util.datetime_util as dtutil
import lib.model.periodoferias as mpf
import lib.model.juncaoperiodos as mjp
import lib.model.calendario as cal

    
def pesquisa(ano, **config):
    '''
    Executa o programa, trazendo as opções, processo base
    '''
    
    def config_read(x, default=None):
        if x in config:
            return config[x]
        return default
    
    verbose = config_read('verbose', False)
    meses_selecionados = config_read('meses')
    tamanhos_oficiais_selecionados = config_read('tamanhos_oficiais')
    faltas_selecionadas = config_read('faltas', [])
    alavancagem_minima = config_read('alavancagem_minima', 1)
    exige_ganho_na_falta = config_read('exige_ganho_na_falta', True)
    
    perido_anual = {}
    for dia in dtutil.dias_do_ano(ano):
        
        if meses_selecionados != None and dia.month not in meses_selecionados:
            continue
        
        perido_anual[ dia ] = []

        #
        #   As ferias devem começar em dia útil.
        # não serve final de semana, feriado ou ponto facultativo
        if not cal.CalFeriadosEFacultativos.eh_dia_util( dia):
            if verbose:
                print '\tFérias devem começar em dia de trabalho!'
            continue

        
        for N in range(1, 26):

            if N == 0:
                if verbose:
                    print '\tFérias de 0 dias é apenas figurativo.'
                continue

            if tamanhos_oficiais_selecionados != None and N not in tamanhos_oficiais_selecionados:
                continue

            #
            #   Gera a opção de ferias para a data e span informados
            pf = mpf.new_periodo_ferias(dia, N)

            #
            #   As férias não podem ter menos de 10 dias corridos
            if pf.dias_corridos_oficiais() < 10:
                if verbose:
                    print 'As férias devem ter pelo menos 10 dias corridos.'
                continue
            
            #
            #   As opções selecionadas não pode ser pior que a opção padrão
            if pf.alavancagem() < alavancagem_minima:
                if verbose:
                    print 'As férias estão piores que o mínimo esperado.'
                continue

            perido_anual[ dia ].append( pf )
            

            for falta in faltas_selecionadas:
                
                for pfs in mjp.gerador_opcoes_com_falha(pf, falta):
                    if pfs == None:
                        continue
    
                    #
                    #   A falha deve valer à pena
                    
                    if pfs.dias_corridos_reais() - pf.dias_corridos_reais() > falta :
                        
                        #print pfs.dias_corridos_reais(), pf.dias_corridos_reais(), pfs.dias_corridos_reais() - pf.dias_corridos_reais(), falta
                        
                        perido_anual[ dia ].append( pfs )
    
    
    for x in perido_anual.keys()[:]:
        if len(perido_anual[ x ]) == 0:
            del perido_anual[ x ]
    
    return perido_anual





