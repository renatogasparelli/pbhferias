#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import datetime
import itertools

from lib.model.roteiroferias import *

OneDay = datetime.timedelta(days=1)


def gerador_roteiros(A, B, di, df):
	
	#
	#
	def distribuir_periodos( cdtrips, dip, dfp ):

		MinDias = 1
	
		di = dip + OneDay
		df = dfp - OneDay
		
	
		def recursive_step( PI, PF, V, idx, Vs):
			
			# o indice refere-se ao vetor e não pode ser maior
			if idx >= len(V):
				return
		
			# sempre maior que o elemento anterior, desde que haja
			if idx > 0:
				if V[idx - 1] + OneDay > PF[idx]:
					return
				V[idx] = V[idx - 1] + MinDias * OneDay
			
			#enquanto for menor que i limite superior, cresca de um em um dia
			while V[idx] <= PF[idx]:
				if idx == len(V) - 1 :
					Vs.append( [dip] + V[:] + [dfp])
					
				# reproduzir para um indice superior
				recursive_step(PI, PF, V, idx+1, Vs)
				V[idx] += MinDias * OneDay
		
		
		PI = [ di + i * OneDay for i in range( cdtrips ) ]
		PF = [ df - ( cdtrips -  i  - 1) * OneDay for i in range( cdtrips ) ]
		V = PI[:]
		Vs = []
		recursive_step( PI, PF, V, 0, Vs)
		
		return Vs
	
	sA = len(A)
	
	roteiros = []
	D = distribuir_periodos( sA - 1, di, df )
	for pA in itertools.permutations(A):
		for d in D:
			#print d
			roteiro = Roteiro()
			roteiro.entry.append( Deslocamento( B, pA[0], di ) )
			for i in range(0,  sA ):
				roteiro.entry.append( Permanencia( pA[i], d[i], d[i+1] ) )
				if i < sA - 1:
					roteiro.entry.append( Deslocamento( pA[i], pA[i+1], d[i+1] ) )
			roteiro.entry.append( Deslocamento( pA[-1], B, df ) )
			
			
			roteiros.append( roteiro )
			
			#print [str(x) for x in roteiro]
	
	return roteiros

