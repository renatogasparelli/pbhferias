#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys


class Parameter(object):
    '''
    '''
    def __init__(self, name, description, sub_parameters=[], **config):
        self.name = name
        self.description = description
        self.sub_parameters = sub_parameters
        self.function = None

    def help(self):
        buf = []
        self._print_me(0, buf)
        print '\n'.join( buf )

    def _print_me(self, deep, buf):
        buf.append( '%s%s' % ( '\t'*deep , str( self ) ) )
        for y in self.sub_parameters:
            y._print_me( deep + 1, buf ) 

    def __str__(self):
        return '%s -> %s' % ( self.name, self.description )


    def lookup(self, key):
        if self.name == key:
            return self
        value = None
        for sp in self.sub_parameters:
            value = sp.lookup(key)
            if value != None:
                break
        return value


class FunctionParameter(Parameter):
    '''
    '''
    def __init__(self, function, name, description, sub_parameters=[], **config):
        Parameter.__init__(self, name, description, sub_parameters, **config)
        self.function = function
    
    def _print_me(self, deep, buf):
        buf.append('')
        Parameter._print_me(self, deep, buf)
        buf.append('')



IntArrayPattern = re.compile('(\d+)\-(\d+)')

class ArgvParser(object):
    '''
    '''
    def __init__(self):
        def cut(x):
            end = len(x)
            if ':' in x:
                end = x.index(':')
            return x[:end]
        #
        # __argv vai conter apenas os nomes das opções
        self.__argv = [ cut(x) for x in sys.argv[1:] ]

    def __iter__(self):
        return iter( self.__argv )

    def plain(self):
        return [ x for x in sys.argv[1:] if x[0] != '-' ]

    def value_of(self, option_name, default_value=None):
        key = '%s:'%option_name
        value = default_value
        for opt in sys.argv:
            if opt.startswith(key):
                value = opt[len(key):]
                break
        return value

    def values_of(self, option_name, default_value=[]):
        value = self.value_of(option_name)
        if value == None:
            return default_value
        #
        # os parametros do formato inteiro-inteiro são expandidos para um array de inteiro
        expanded_value = []
        for i in value.split(','):
            m = IntArrayPattern.match(i)
            if m:
                menorInt = int(m.group(1))
                maiorInt = int(m.group(2))
                if menorInt < maiorInt:
                    for x in range(menorInt, maiorInt + 1):
                        expanded_value.append( str(x) )
            else:
                expanded_value.append(i)
        #print expanded_value
        return expanded_value


    def bounded_values_of(self, option_name, bound_values, default_value=[]):
        values = self.values_of(option_name, default_value)
        if len(values) == 0 or values == default_value:
            return default_value
        bound_values = str_value( bound_values )
        #
        # as opções estão limitadas ao que aparece na lista  bound_values
        return [ x for x in values if x in bound_values ]

    def unknow_option(self, parameters):
        values = []
        for opt in self:
            if opt[0] == '-' and parameters.lookup(opt) == None:
                values.append(opt)
        return values


class UserOptions( ArgvParser ):
    '''
    '''
    
    def __init__(self, parameters):
        ArgvParser.__init__(self)
        self.parameters = parameters
        if self.parameters.lookup('-help') == None:
            self.parameters.sub_parameters.append(
                FunctionParameter( self.parameters.help , '-help', 'Exibe as opções do programa' )
            )
        self.verify()


    def verify(self):
        
        help_and_exit = '-help' in self
    
        unknow_option = self.unknow_option(self.parameters)
        if len(unknow_option) > 0:
            for x in unknow_option:
                print 'Opção desconhecida: %s' % x
            print ''
            help_and_exit = True
    
    
        if help_and_exit:
            self.parameters.help()
            sys.exit(0)

    def run(self):
        
        houve_execucao = False
        for x in self:
            opt = self.parameters.lookup(x)
            if opt != None and isinstance(opt, FunctionParameter):
                opt.function( )
                houve_execucao = True
    
        if not houve_execucao:
            self.parameters.help()


def __to_type( x, ttype ):
    if x == None:
        return None
    if isinstance(x, list):
        return [ ttype(i) for i in x ]
    return ttype(x)

def int_value(x): return __to_type(x, int)
def str_value(x): return __to_type(x, str)
def float_value(x): return __to_type(x, float)