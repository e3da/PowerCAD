'''
Created on Feb 26, 2017

@author: qmle
Functions for simple curve_fitting
'''
import numpy as np
import math as m


def f1 (f=1,a=1,b=1): 
    ''' this one is used to curve fit AC inductance v.s frequency'''
    return a*np.log(f)+ b

def f2 (f=1,a=1,b=1):
    ''' this one is used to curve fit AC inductance v.s frequency'''
    return a+b/f

def f3 (f=1,a=1,b=1,c=1):
    ''' this one is used to curve fit AC Resistance v.s frequency'''
    return a*f**2+b*f+c