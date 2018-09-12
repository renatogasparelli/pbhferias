#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from datetime import date, timedelta

#
# "Try Not to Laugh Challenge: Family Guy Edition"
#       https://www.youtube.com/watch?v=_B4MoqrIEL4
#
# "Best of Peter Griffin [HD]"
#       https://www.youtube.com/watch?v=RTwv9bkVUWA
#
# https://www.carrefour.fr/ =>  "eau minérale"
# https://www.carrefour.it/ =>  "acqua minerale"
# https://www.carrefour.es/ =>  "agua mineral"
#
# Studio Apartment Vicolo Lavandai

def main():
        
    plano1 = [
        Deslocamento( BeloHorizonte, Barcelona   , J04      , 4285 * BRL, 'Aviao' ),
        Hospedagem  ( Barcelona                  , J05, J09 , 1140 * BRL, 'Petit Mirador'),
        Deslocamento( Barcelona  , CapDAgde      , J09      ,  100 * BRL, 'Carro' ),
        Hospedagem  ( CapDAgde                   , J09, J13 , 1458 * BRL, 'Hotel Les Grenadines'),
        Deslocamento( CapDAgde   , Nice          , J13      ,  100 * BRL, 'Carro' ),
        Hospedagem  ( Nice                       , J13, J17 , 1458 * BRL, 'Hotel des Dames'),
        Deslocamento( Nice       , Milan         , J17      ,  100 * BRL, 'Carro' ),
        Hospedagem  ( Milan                      , J17, J22 , 1516 * BRL, 'Studio Apartment Vicolo Lavandai'),
        Deslocamento( Milan      , BeloHorizonte , J22      , 4285 * BRL, 'Aviao' ),
    ]
   
    plano2 = [
        
        Deslocamento( BeloHorizonte, Barcelona   , M31      , 4285 * BRL, 'Aviao' ),
        Hospedagem  ( Barcelona                  , J01, J06 , 1592 * BRL, ''),
        Deslocamento( Barcelona  , CapDAgde      , J06      ,  100 * BRL, 'Carro' ),
        Hospedagem  ( CapDAgde                   , J06, J11 , 1823 * BRL, ''),
        Deslocamento( CapDAgde   , Nice          , J11      ,  100 * BRL, 'Carro' ),
        Hospedagem  ( Nice                       , J11, J16 , 1823 * BRL, ''),
        Deslocamento( Nice       , Florenca      , J16      ,  100 * BRL, 'Carro' ),
        Hospedagem  ( Florenca                   , J16, J21 , 1675 * BRL, ''),
        Deslocamento( Florenca   , Milan         , J21      ,  100 * BRL, 'Carro' ),
        Hospedagem  ( Milan                      , J21, J28 , 1800 * BRL, ''),
        Deslocamento( Milan      , BeloHorizonte , J28      , 4285 * BRL, 'Aviao' ),
    ]
    
    avalie_planos( plano2 )


def avalie_planos( plano ):
    
    def formata_moeda(x):
        q = int(x)
        r = (x - q) * 100
        
        sq = ''
        while True:
        
            if q < 1000:
                sq = '%d'%q + sq
                break
            else:
                tq = q%1000
                sq = '.%03d'%tq + sq
                q = q/1000
            
            
        return 'R$ %s,%02d'%(sq, r)    
    
    pi = 1
    for ri in expandir_rotas( plano ):
        print 'Rota', pi
        
        i = 1
        total = 0
        for rii in ri:
            crii = rii.custo()
            print '\t%02d -'% i, rii.info(), formata_moeda(crii)
            i += 1
            total += crii
            
        print '\t', '     =====> Custo Total = ', formata_moeda(total)
        
        pi += 1
    
    print ''


def expandir_rotas(rotas):
    
    qtt = 1
    for i in rotas:
        if isinstance(i, list):
            qtt *= len(i)
    
    rotas_alternativas = [ [] for i in range(qtt) ]
    
    for ri in rotas:
        if isinstance(ri, list):
            j = 0
            li = len(ri)
            for ra in rotas_alternativas:
                ra.append( ri[ j%li ] )
                j+=1
        else:
            for ra in rotas_alternativas:
                ra.append( ri )

    
    for ra in rotas_alternativas:
        yield ra
    

class Hospedagem:
    
    def __init__(self, cidade, dt_entrada, dt_saida, vlr_total_hotel, nome):
        self.cidade = cidade
        self.nome = nome
        self.vlr_total_hotel = vlr_total_hotel
        self.dt_entrada = dt_entrada
        self.dt_saida = dt_saida
        self.dias = (self.dt_saida - self.dt_entrada).days
    
    def custo_diario(self):
        return (  4 * self.cidade.vlr_bigmac # 4 unidades, dois para mim e dois para nanan
                + 4 * self.cidade.vlr_litro_agua # 4 litros, dois para mim e dois para a nanan
                )

    def custo(self):
        return (self.dias * self.custo_diario()) + self.vlr_total_hotel

    def info(self):
        return 'Estadia em %s [%s]'%( self.cidade.nome, self.nome )

class Deslocamento:
    
    def __init__(self, cidade_origem, cidade_destino, dt_passagem, vlr_passagem, modal):
        self.cidade_origem = cidade_origem
        self.cidade_destino = cidade_destino
        self.dt_passagem = dt_passagem
        self.vlr_passagem = vlr_passagem
        self.modal = modal

    def custo(self):
        return self.vlr_passagem

    def info(self):
        return 'Viagem de %s para %s [%s]'%( self.cidade_origem.nome, self.cidade_destino.nome, self.modal )

class Cidade:
    
    def __init__(self, nome, vlr_bigmac, vlr_litro_agua):
        self.nome = nome
        self.vlr_bigmac = vlr_bigmac
        self.vlr_litro_agua = vlr_litro_agua

class CidadeSede:
    
    def __init__(self, nome):
        self.nome = nome


BRL = 1
EUR = 4.014
ONE_DAY = timedelta(days=1)


BeloHorizonte = CidadeSede('Belo Horizonte')
Barcelona = Cidade('Barcelona', 7 * EUR, 0.6 * EUR)
CapDAgde  = Cidade('CapDAgde' , 8 * EUR, 0.6 * EUR)
Nice      = Cidade('Nice'     , 8 * EUR, 0.6 * EUR)
Cannes    = Cidade('Cannes'   , 8 * EUR, 0.6 * EUR)
Florenca  = Cidade('Florenca' , 8 * EUR, 0.6 * EUR)
Milan     = Cidade('Milan'    , 8 * EUR, 0.6 * EUR)



M31 = date(2018, 05, 31)
J01 = M31 + ONE_DAY *  1
J02 = M31 + ONE_DAY *  2
J03 = M31 + ONE_DAY *  3
J04 = M31 + ONE_DAY *  4
J05 = M31 + ONE_DAY *  5
J06 = M31 + ONE_DAY *  6
J07 = M31 + ONE_DAY *  7
J08 = M31 + ONE_DAY *  8
J09 = M31 + ONE_DAY *  9
J10 = M31 + ONE_DAY * 10
J11 = M31 + ONE_DAY * 11
J12 = M31 + ONE_DAY * 12
J13 = M31 + ONE_DAY * 13
J14 = M31 + ONE_DAY * 14
J15 = M31 + ONE_DAY * 15
J16 = M31 + ONE_DAY * 16
J17 = M31 + ONE_DAY * 17
J18 = M31 + ONE_DAY * 18
J19 = M31 + ONE_DAY * 19
J20 = M31 + ONE_DAY * 20
J21 = M31 + ONE_DAY * 21
J22 = M31 + ONE_DAY * 22
J23 = M31 + ONE_DAY * 23
J24 = M31 + ONE_DAY * 24
J25 = M31 + ONE_DAY * 25
J26 = M31 + ONE_DAY * 26
J27 = M31 + ONE_DAY * 27
J28 = M31 + ONE_DAY * 28
J29 = M31 + ONE_DAY * 29
J30 = M31 + ONE_DAY * 30

if __name__ == '__main__':
    main()
