#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import lib.util.feriados as fer
import lib.util.dbclient as db
import gear

import itertools


FOR_REAL = False

def main():
    upto25()
    delete_all()
    insert_eventos_calendario()
    insert_calendario()
    insert_opcao_ferias()


def insert_opcao_ferias():
    inserts = []
    for ano in gear.anos():
        for pf in gear.generate_regular_options( ano ):
            
            s = '( to_date(\'%s\', \'YYYY-MM-DD\'), to_date(\'%s\', \'YYYY-MM-DD\'), \
                    to_date(\'%s\', \'YYYY-MM-DD\'), to_date(\'%s\', \'YYYY-MM-DD\') , \
                    %d, %d, %d, %d, %d, %d, %f )' % (
                        pf.foi, pf.fof, pf.fri, pf.frf, pf.N,
                        pf.dias_corridos_oficiais(), pf.dias_corridos_reais(),
                        pf.dias_uteis_oficiais(), pf.dias_uteis_reais(),
                        pf.dias_corridos_esperados(), pf.alavancagem() )
        
            inserts.append(s)

    statement =  'insert into ferias.opcao_ferias ( dt_oficial_inicial, dt_oficial_final, \
                 dt_real_inicial, dt_real_final, tamanho, \
                 dias_corridos_oficiais, dias_corridos_reais, dias_uteis_oficiais, dias_uteis_reais,\
                 dias_corridos_esperados, alavancagem \
                 ) values \n'
    
    for insert in inserts[:-1]:
        statement += insert + ',\n'
    
    statement += inserts[-1] + ';\n'
    
    exec_statement( statement )
    

def insert_calendario():
    inserts = []
    for ano in gear.anos():
        
        for evento in fer.feriados_bh(ano):
            s =  '(1, to_date(\'%s\', \'YYYY-MM-DD\') , \'%s\')' % (  evento.dia, evento.titulo )
            inserts.append(s)
                
        for evento in fer.facultativos_comuns(ano):
            s =  '(2, to_date(\'%s\', \'YYYY-MM-DD\') , \'%s\')' % (  evento.dia, evento.titulo )
            inserts.append(s)
            
        for evento in fer.facultativos_desejados(ano):
            s =  '(3, to_date(\'%s\', \'YYYY-MM-DD\') , \'%s\')' % (  evento.dia, evento.titulo )
            inserts.append(s)
    
    
    statement =  'insert into ferias.calendario (tipo, dt_dia, descricao) values \n'
    for insert in inserts[:-1]:
        statement += insert + ',\n'
    statement += inserts[-1] + ';\n'
    
    exec_statement( statement )


def insert_eventos_calendario():
    statement =  'insert into ferias.eventos_calendario (id, descricao) values \n'
    statement += '( 1, \'feriados propriamente dito\') ,\n'
    statement += '( 2, \'ponto facultativo comum\') ,\n'
    statement += '( 3, \'ponto facultativo desejado\') ;'
    
    exec_statement( statement )
    

def delete_all():
    exec_statement( 'delete from ferias.opcao_ferias;' )
    exec_statement( 'delete from ferias.calendario;' )
    exec_statement( 'delete from ferias.eventos_calendario;' )
    

def exec_statement( statement ):    
    if not FOR_REAL:
        print statement
        return
    db.PessoalLocal.connect()
    db.PessoalLocal.execute( statement )
    db.PessoalLocal.close()
        


def upto25():
    Base = range(26)
    values = []
    for i, j, k in itertools.product( Base, Base, Base ):
        if ( i + j + k ) != 25:
            continue
        values.append( '( %d, %d, %d )\n' % ( i, j, k ) )

    statement =  'insert into ferias.upto25 (periodo1, periodo2, periodo3) values %s ; \n'
    exec_statement( 'delete from ferias.upto25;' );
    exec_statement( statement % ', '.join( values ) )


if __name__ == '__main__':
    main()
