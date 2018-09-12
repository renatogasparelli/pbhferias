#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Pela regras as ferias contituem 25 dias uteis por ano,
    podendo ser divididas em até dois periodos não inferiores a 10 dias corridos.
'''

import datetime

import lib.util.datetime_util as dtutil
import lib.util.feriados as fer
import lib.model.oportunidades as oportunidades
import lib.model.juncaoperiodos as mjp
import lib.model.periodoferias as perfer
import lib.model.restricoes as restr

DistanciaMinimaEntrePeriodosDeFerias = 100

from lib.util.hargv import *

def main(): args.run()

#
# /usr/local/lib/python2.7/dist-packages/renatogc
#

def lista():
    '''
    Trabalha com opção a opção de férias, trazendo as opções de aproveitamento para cada dia do ano
    '''
    
    def eh_opcao_admissivel(opt):
        
        #
        # se a falta ocorrer depois da folha entregue, não posso
        #   tentar abonar 'justificando' no sistema
        if ( isinstance(opt, mjp.JuncaoPeriodoFerias) and not opt.faltas_apenas_no_retorno() ):
            return False
    
        return True
    
    criterio_ordenacao = args.bounded_values_of('-ordem', OrdenePorOpcoes, [ OrdenePorOpcoes[0] ])
    
    def report(perido_anual, alavancagem_minima, aproveitados_minimo):
        
        #
        #   primeiro ordene por dia
        dias_ordenados = sorted(perido_anual.keys())
        
        sort_methods = {
            'aproveitados': lambda x: max( [ y.dias_corridos_reais() for y in perido_anual[x] ] ),
            'alavancagem' : lambda x: max( [ y.alavancagem() for y in perido_anual[x] ] ),
        }
        
        for sort_method_key in criterio_ordenacao:
            if sort_method_key == 'dia': continue
            sort_method = sort_methods[sort_method_key]
            dias_ordenados = sorted(dias_ordenados, key=sort_method )
        
    
        cnt = 1
        report = []
        for dia in dias_ordenados:
            
            subreport = []
            for opcao in perido_anual[dia]:
                
                if ( opcao.alavancagem() < alavancagem_minima
                    or opcao.dias_corridos_reais() < aproveitados_minimo 
                    or not eh_opcao_admissivel(opcao) ):
                    continue
                
                subreport.append('\n\tPosição geral[%03d]'%cnt)
                cnt += 1
                if VisaoTecnica:
                    subreport.append( opcao.printme() )
                else:
                    subreport.append( opcao.reportme(Detalhe) )
            
            if len(subreport) > 0:
                report.append( '' )
                report.append( dtutil.formata_data_ptbr(dia) )
                report.extend( subreport )
                    
    
        return '\n'.join( report )


    #
    # pode ser passado o valor de alavancagem minima ou dias minimo
    minimo_referencia = float_value( args.value_of('-lista', 1.00001) )
    if minimo_referencia < 3:
        alavancagem_minima =  float( minimo_referencia )
        aproveitados_minimo = 0
    else:
        alavancagem_minima = 0
        aproveitados_minimo = int( minimo_referencia )
        
        
    
    
    config = {
        'meses' : int_value( args.bounded_values_of('-per', MesesBase, MesesBase) ),
        'tamanhos_oficiais' : int_value( args.bounded_values_of('-tamo', PeriodosBase, PeriodosBase) ),
        'faltas' : int_value( args.bounded_values_of('-faltas', FaltasAdmitidasBase) ),
        'alavancagem_minima' : alavancagem_minima,
        'exige_ganho_na_falta' : True,
        'verbose':False
    }
    
    #print args.value_of('-saida', 'ola')
    
    
    
    #
    # algo está senco acumulado aqui???
    for i in AnosSelecionados:
        perido_anual = {}
        perido_anual.update(oportunidades.pesquisa(i, **config))
        print report(perido_anual, alavancagem_minima, aproveitados_minimo)


        
def combos():
    '''
    Trabalha com composições de férias, pensando no melhor aproveitamento anual
    '''
    
    faltas_admitidas = int_value( args.bounded_values_of('-faltas', FaltasAdmitidasBase) )
    
    def obter_faltas(x):
        if isinstance(x, mjp.JuncaoPeriodoFerias):
            return x.faltas()
        return 0
    
    def eh_opcao_admissivel(opt, meses_selecionados_limites):
        #
        # ignore as opções iniciadas fora do período selecionado
        if not restr.data_pertencente_aos_periodos( opt.foi, meses_selecionados_limites ):
            return False
        
        #
        # se a falta ocorrer depois da folha entregue, não posso
        #   tentar abonar 'justificando' no sistema
        if ( isinstance(opt, mjp.JuncaoPeriodoFerias) and not opt.faltas_apenas_no_retorno() ):
            return False
    
        return True
    
    def report(perido_anual, tamanho_combo_minimo,
               meses_p1_limites, meses_p2_limites):
        
        #
        # Organiza as entradas de acordo com o size número de dias úteis
        #   do período
        agrupados_por_tamanho = {}
        for x in [ opt for opts_do_dia in perido_anual.values() for opt in opts_do_dia ]:
            if x.size() not in agrupados_por_tamanho:
                agrupados_por_tamanho[ x.size() ] = []
            agrupados_por_tamanho[ x.size() ].append( x )
            
            #if len(agrupados_por_tamanho) == 10: break
        
        #
        # 
        evaluated = set([])
        composicoes = {}
        
        #
        # as instancias de períodos férias foram agrupadas pelo tamanho
        #   de dias úteil e serão agora unidas como composição da combo
        for r in sorted(agrupados_por_tamanho.keys()):
            
            if r in evaluated:
                continue
            
            #
            # deriva o valor do restante das férias a serem tiradas
            s = 25 - r
            evaluated.add(s)
        
            
            if r == 25:
                
                #
                # um resultado que considera o total de 25 dias
                #   corridos de férias
                for optr in agrupados_por_tamanho[r]:
                    
                    if not eh_opcao_admissivel(optr, meses_p1_limites): continue
                    
                    total = optr.dias_corridos_reais()
                    if total < tamanho_combo_minimo:
                        continue

                    if total not in composicoes:
                        composicoes[total] = []
                    composicoes[total].append( [ optr ] )
        
            #
            # se houver algum período para esse tamanho
            elif s in agrupados_por_tamanho.keys():
                
                #
                # obtem as opções para o tamanho R
                for optr in agrupados_por_tamanho[r]:
                    
                    if not eh_opcao_admissivel(optr, meses_p1_limites): continue
                        
                    
                    faltas_optr = obter_faltas( optr )
                    #
                    # obtem as opções para o tamanho S
                    for opts in agrupados_por_tamanho[s]:
                        
                        if not eh_opcao_admissivel(opts, meses_p2_limites): continue
                        
                        #
                        # avalia se ha colisão entre os períodos
                        #   Ignore se sim
                        if perfer.periodos_colidem( optr, opts ):
                            continue                      
                        
                        #
                        # havendo a opção de se admitir que se falta ao trbalho alguns dias
                        #   controle de combo, as opções respeitam a quantidade de faltas
                        #
                        #   -> ANTES O CONTROLE ERA POR ANO, HJ É POR MÊS, POSSO FALTAR MAIS...
                        #               ATÉ DUAS VEZES POR MÊS POSSO ESQUECER O CRACHA! :-)
                        #
                        #faltas_totais = faltas_optr + obter_faltas( opts )
                        #if faltas_totais > 0 and faltas_totais not in faltas_admitidas:
                        #    continue
                        
                        #
                        # avalia se a soma dos períodos é maior que o mínimo
                        total = optr.dias_corridos_reais() + opts.dias_corridos_reais()
                        if total < tamanho_combo_minimo:
                            continue
                        
                        opt1, opt2 = perfer.ordena(optr, opts)
                        
                        #
                        # separe as ferias em pelo menos 100 dias
                        if perfer.distancia( opt1, opt2 ) < DistanciaMinimaEntrePeriodosDeFerias:
                            continue
                        
                        #
                        # inclui na coleção de períodos
                        if total not in composicoes.keys():
                            composicoes[total] = []
                        composicoes[total].append( [ opt1, opt2 ] )
                        
        
        #
        #   Exibe o resultado, organizado pelo valor da soma
        rep = []
        
        cid = 1
        for total in sorted(composicoes.keys()):
            
            for composicao in composicoes[total]:
                
                rep.append( '*'*80 )
                
                #
                # a compisicao de tamanho 1 ocorre quando se tira todas as
                #   férias de uma tacada apenas
                if len(composicao) == 1:
                    rep.append( 'Opcao [%03d]: %02d  com %02d'% (cid, composicao[0].size(), total) )
                else:
                    rep.append( 'Opcao [%03d]: %02d e %02d com %02d'% (cid, composicao[0].size(), composicao[1].size(), total) )
                
                cid += 1
                
                for item in composicao:
                        if VisaoTecnica:
                            rep.append( item.printme() )
                        else:
                            rep.append( item.reportme(Detalhe) )
                
        
        return '\n'.join( rep )
    
    tamanhos_oficiais = int_value( args.bounded_values_of('-tamo', PeriodosBase, PeriodosBase) )
    for r in tamanhos_oficiais[:]:
        if r == 25: continue
        s = 25 - r
        if s not in tamanhos_oficiais:
            tamanhos_oficiais.append(s)
    
    tamanho_combo_minimo = int_value( args.value_of('-combos', 47) )
    
    #
    # default: todos os meses são selecionados
    meses_p1 = int_value( args.bounded_values_of('-per1', MesesBase, MesesBase) )
    meses_p2 = int_value( args.bounded_values_of('-per2', MesesBase, MesesBase) )    
    meses_p1_limites = []
    meses_p2_limites = []
    
    for i in AnosSelecionados:
        for j in meses_p1:
            meses_p1_limites += [ dtutil.limites_do_mes( i, j ) ]
        for j in meses_p2:
            meses_p2_limites += [ dtutil.limites_do_mes( i, j ) ]
            

    config = {
        'meses' : MesesBase, # os meses informados são utilizados para formação do campo
        'tamanhos_oficiais' : tamanhos_oficiais,
        'faltas' : faltas_admitidas,
        'alavancagem_minima' : -1,
        'exige_ganho_na_falta' : False,
        'verbose':False
    }
    
    for i in AnosSelecionados:
        data = oportunidades.pesquisa(i, **config)
        print report(data, tamanho_combo_minimo,
               meses_p1_limites, meses_p2_limites) 
    
def calendario():
    '''
    exibe o calendário
    '''
    buf = []
    for i in AnosSelecionados:
        calendario = sorted( fer.calendario( i ),  key=lambda x:x.dia)
        for x in calendario:
            buf.append( '\t%s' % str(x) )
    print '\n'.join( buf )




def dummy():pass









AnosBase = range(2015, dtutil.THIS_YEAR + 10)
MesesBase = range(1, 13)
FaltasAdmitidasBase = [ 1, 2 ]
PeriodosBase = range(26)
OrdenePorOpcoes = ['dia', 'alavancagem', 'aproveitados']

Opcoes_lista = [
    Parameter('-anos', 'Uso: -anos[:[<ano>,<ano>,...,<ano>|<ano>-<ano>]]. Default: ano seguinte'),
    Parameter('-detalhe', 'Inclui os detalhes da opção'),
    Parameter('-faltas', 'Faltas admitidas => %s'%','.join( str_value( FaltasAdmitidasBase) )),
    Parameter('-tec', 'Exibe relatorio, visão tecnica'),
    Parameter('-tamo', 'Tamanho oficial das férias => %s'%','.join( str_value( PeriodosBase))),
]

Parameters = Parameter( sys.argv[0], 'Programa de apoio ao planejamento de ferias',
    [
        FunctionParameter(lista, '-lista',
            'Traz a lista de opções de férias. -lista:[mínimo de referência: se < 3: alavancagem; senão: dias]',
            Opcoes_lista + [            
                Parameter('-per', 'Meses de interesse => %s'%','.join( str_value( MesesBase ))),
                Parameter('-ordem', 'Criterio de ordenação [default:dia] => %s'%','.join( OrdenePorOpcoes )),
                
            ]
        ),
        FunctionParameter(combos, '-combos',
            'Traz a lista de combos de opções de férias. -combos:[tamanho minimo da combo]',
            Opcoes_lista + [
                Parameter('-per1', 'Meses de interesse primeiro período => %s'%','.join( str_value( MesesBase))),
                Parameter('-per2', 'Meses de interesse segundo período => %s'%','.join( str_value( MesesBase))),
            ]
        ),
        FunctionParameter(calendario, '-calendario', 'Exibe o calendário de folgas do ano.' ),
        FunctionParameter(dummy, '-saida', '-saida:<nome do arquivo>' ),
    ]
)

args = UserOptions( Parameters )


AnosSelecionados = int_value( args.bounded_values_of('-anos', AnosBase, [ dtutil.THIS_YEAR + 1 ] ))
VisaoTecnica = '-tec' in args
Detalhe = '-detalhe' in args






if __name__ == '__main__':
    command = ' '.join(sys.argv)
    print command
    main()
    print command
