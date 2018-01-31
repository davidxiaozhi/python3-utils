#!/usr/bin/python
#-*- coding: utf-8 -*-

import numpy as np

"""
    rate : 每个阶段的比率
        
    nper : 总共阶段
    
    pmt : Payment 首付款
    pv :  折现
    
    when : {{'begin', 1}, {'end', 0}}, {string, int}, optional
        When payments are due ('begin' (1) or 'end' (0)).
        Defaults to {'end', 0}.
    
    
     The future value is computed by solving the equation::

     fv +
     pv*(1+rate)**nper +
     pmt*(1 + rate*when)/rate*((1 + rate)**nper - 1) == 0

    or, when ``rate == 0``::

     fv + pv + pmt * nper == 0
"""
rate = 0.05
nper = 40
pmt = 14000.0
pv  = 14000.0
money = np.fv(rate=rate, nper=nper-1, pmt=-pmt, pv=-pv)
print("{}年后,你的投入{} 在利率是{} 的情况下,你的收入将会是{}".format(nper, pmt, rate, money ))
# 一年投资次数
c=1
#每月固定投资钱
p=14000
#年化收益利率
i=0.05
#总投资年数
year=40 -1

