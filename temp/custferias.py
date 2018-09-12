#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import datetime

from lib.control.alternativasroteiros import *

'''
Romanticas80
https://www.youtube.com/watch?v=wORn39IH3Ek

Phil Collins - Against All Odds
Jim Diamond - TRADUÇÃO - I Should Have Known Better
Century - Lover Why - HD TRADUÇÃO
Simply Red - You Make Me Feel Brand New
Simply Red - Holding Back The Years (Live HD) Legendado em PT- BR
Annie Lennox - Why (Tradução)
Billy Joel - Uptown Girl
Phil Collins - You Can't Hurry Love
Michael Jackson - The Way You Make Me Feel
Police - Every Breath You Take
Men At Work - Down Under
Will To Power - Freebird...Baby I Love Your Way
Spandau Ballet - True

'''
def main():


	A = ['Barcelona', 'Bordeaux', 'Milan', 'Atenas']
	B = 'Belo Horizonte'
	
	di = datetime.date(2018, 1, 1)
	df = datetime.date(2018, 1, 10)


	for roteiro in gerador_roteiros( A, B, di, df ):
		print roteiro, roteiro.custo()






if __name__ == '__main__':
	main()