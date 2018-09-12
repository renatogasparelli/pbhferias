#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


shift=33

acm = 0

#1-54,

pages=[]
for x in re.compile('(\d+)\-(\d+)').finditer( '348-366,384-399,411-447,560-567,639-676' ):
    chp = ( int(x.group(1))  + shift , int(x.group(2)) + shift )
    acm += ( chp[1] - chp[0] ) + 1
    pages.append(  '%d-%d' % chp  )

print acm
print ','.join( pages )