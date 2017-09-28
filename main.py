# -*- coding: utf-8 -*-
# @Time    : 2016/12/4 下午1:31
# @Author  : Zhixin Piao
# @Email   : piaozhx@seu.edu.cn

from seulex import Lex
from seuyacc import Yacc

lex = Lex('config/minic.l')
tokens = lex.feedCode('test/test.cpp')

terminals = lex.getTerminals()
yacc = Yacc('config/minic.y', terminals)
yacc.feedTokens(tokens)
