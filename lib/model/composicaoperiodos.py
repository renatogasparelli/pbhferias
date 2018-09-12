#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lib.util.datetime_util as dtutil
import lib.model.calendario as cal
import lib.model.periodoferiasbase as pfb

class ComposicaoPeriodos ( pfb.AbsPeriodoFerias ):
    def termo(self): return 'Composição Períodos'
    
    def __init__(self, pfs):        
        self.pfi = pfs[0]
        self.pff = pfs[-1]
        pfb.AbsPeriodoFerias.__init__(self, self.pfi.N + self.pff.N
                                      , self.pff.foi, self.pff.fof
                                      , self.pfi.fri, self.pff.frf, None)
        self.pfs = pfs
        
        self.ref = None
        for x in self.pfs:
            if isinstance(x, pfb.PeriodoFeriasPremio) or isinstance( x, pfb.PeriodoFeriasRegulamentar):
                self.ref = x
                break
        
    def __str__(self):
        lines = [ '%02d de %s ate %s' % ( self.dias_corridos_reais(), self.fri, self.frf ) ]
        lines.extend( [ str(x) for x in self.pfs ]  )
        return '\n'.join( lines )
    

def falta_coberto( cp ):
    
    diasfaltas = []
    for ff in  cp.pfs:
        if not isinstance( ff, pfb.FaltaFerias):
            continue
        for d in cal.CalFeriadosEFacultativos.dias_uteis( ff.foi, ff.fof ):
            diasfaltas.append( d )
    
    # dia de retorno ao trabalho
    retday = cp.frf + dtutil.ONE_DAY
    
    #
    # se o dia de retorno for o primeiro dia util do mês de retorno
    #   então entendo que possam ser "tratadas as faltas do mês e do mês anterior"
    mdi, mdf = dtutil.limites_do_mes( retday.year, retday.month )
    
    duteis = cal.CalFeriadosEFacultativos.conta_dias_uteis( mdi, retday )
    
    def samemonth( d1, d2 ):
        return d1.year == d2.year and d1.month == d2.month
    
    def pastmonth( d1, d2 ):
        if d1.year == d2.year:
            return abs( d1.month - d2.month ) == 1
        elif ( d1.year == d2.year + 1 and d1.month == 0 and d2.month == 11 ):
            return True
        elif ( d1.year + 1 == d2.year and d2.month == 0 and d1.month == 11 ):
            return True
        return False
        
    
    if duteis == 1: # próprio dia!
        for d in diasfaltas:
            if not ( samemonth( retday, d ) or pastmonth( retday, d ) ):
                return False
    
    else:
        for d in diasfaltas:
            if not samemonth( retday, d ):
                return False

    return True
    
    


'''    
A opção de férias final deve começar depois da opção de férias inicial, o limite acontece quando:
    1 - [ pi.fof < pf.foi ] e [ pi.frf >= pf.fri ]
       _______________________
     /     /           \      \
 pi.fri  pi.foi     pi.fof   pi.frf
                          _______________________
                        /      /         \       \
                    pf.fri  pf.foi     pf.fof   pf.frf
                        
    2 - (pi.fof == pi.frf) and ( pf.fof == pf.frf ) and ((pf.foi - pi.fof).days == 1)  
'''
def eh_admissivel_concatenar( pfs ):
    
    def is_valid( pi, pf ):
        
        if pi == None or pf == None:
            return False
        
        if pi.fof < pf.foi and pi.frf >= pf.fri:
            return True
        
        if ( pi.fof == pi.frf ) and ( pf.fof == pf.frf ) and ((pf.foi - pi.fof).days == 1):
            return True
        
        return False


    x = pfs[0]
    for i in range(1, len(pfs)):
        y = pfs[i]
        if not is_valid(x, y):
            return False
        x = y
    
    return True


# END