#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import psycopg2


class PostgreeSql(object):
    
    def __init__(self, host, dbname, user, password):
        #self.conn = psycopg2.connect("host='10.27.10.200' dbname='cart' user='desenv' password='desenv'")
        self.connstr = "host='%(host)s' dbname='%(dbname)s' user='%(user)s' password='%(password)s'"%{
            'host':host, 'dbname':dbname, 'user':user, 'password':password
        }
        self.conn = None
        
    def connect(self):
        self.conn = psycopg2.connect(self.connstr)
    
    def select_one(self, x):
        if self.conn == None:
            return None
        cursor = self.conn.cursor()
        cursor.execute(x)
        return cursor.fetchone()
    
    def select(self, x):
        if self.conn == None:
            return None
        cursor = self.conn.cursor()
        cursor.execute(x)
        return cursor.fetchall()
    
    def execute(self, x):
        if self.conn == None:
            return None
        cursor = self.conn.cursor()
        cursor.execute(x)
        self.conn.commit()
    
    def close(self):
        self.conn.close()
    


PessoalLocal = PostgreeSql( 'localhost', 'pessoal', 'postgres', 'postgres' )


