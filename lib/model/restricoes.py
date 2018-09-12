#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


def data_pertencente_aos_periodos(x, periodos):
    for iper, fper in periodos:
        if  iper <= x <= fper:
            return True
    return False



