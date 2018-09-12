#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import datetime
import collections
import json

from lib.util.algorithms import *

Destino = collections.namedtuple('Destino', 'nome agua bigmac hotels')
Hotel = collections.namedtuple('Hotel', 'nome diaria traslado')

Deslocamento = collections.namedtuple('Deslocamento', 'origem destino meios')
Meio = collections.namedtuple('Meio', 'companhia modal duracao precos')
Preco = collections.namedtuple('Preco', 'data valor')

@Singleton
class ContextInfo:
	
	def __init__(self):
		with open('dados/destinos.json') as fp:
			self.destinos_data = json.load(fp)
		
		self.destinos = {}
		for x in self.destinos_data:
			destino = Destino(**x)
			self.destinos[ destino.nome ] = destino
		
		with open('dados/deslocamento.json') as fp:	
			self.descolamento_data = json.load(fp)
		
		self.deslocamentos = {}
		for x in self.descolamento_data:
			deslocamento = Deslocamento(**x)
			self.deslocamentos[ (deslocamento.origem , deslocamento.destino) ] = deslocamento
	
	def city_of(self, x):
		return self.destinos[x];

	def ticket_for(self, x, y, d):
		for m in self.deslocamentos[(x, y)].meios:
			meio = Meio(**m)
			for p in meio.precos:
				preco = Preco(**p)
				return preco
		return None

	def hotel_at(self, x):
		return Hotel(**self.city_of(x).hotels[0])
	


	
Infoset = ContextInfo.Instance()


class Roteiro:
	
	def __init__(self):
		self.entry = []

	def __str__(self):
		return ' => '.join([str(x) for x in self.entry if isinstance(x, Deslocamento)])

	def custo(self):
		return sum( [ x.custo() for x in self.entry ] )
	

class Permanencia:
	
	def __init__(self, local, inicio, termino):
		self.local = local
		self.inicio = inicio
		self.termino = termino
	
	def custo(self):
		
		dias = (self.termino - self.inicio).days + 1
		
		return (
			dias * Infoset.hotel_at( self.local ).diaria +
			dias * Infoset.city_of( local ).agua +
			dias * Infoset.city_of( local ).bigmac +
			Infoset.city_of( local ).verba_especifica
		)
	
	def __str__(self):
		return '%s [ %s -> %s ]'%(self.local, self.inicio, self.termino)


class Transporte:
	
	def __init__(self, origem, destino, data):
		self.origem = origem
		self.destino = destino
		self.data = data

	def custo(self):
		
		return (
			Infoset.hotel_at( self.origem ).traslado +
			Infoset.ticket_for( self.origem, self.destino, self.data ).preco +
			Infoset.hotel_at( self.destino ).traslado
		)
		


	def __str__(self):
		return '%s -> %s [ %s ]'%(self.origem, self.destino, self.data)

