# -*- coding: utf-8 -*-
# @Time    : 2016/12/4 下午2:48
# @Author  : Zhixin Piao 
# @Email   : piaozhx@seu.edu.cn

from LR import LR1

names = {}


class Yacc:
    def __init__(self, path, terminals):
        self.terminals = terminals
        with open(path, 'r') as f:
            self.parserYaccFile(f.read())

    # 读取lex文件信息
    def parserYaccFile(self, content):
        # 定义区，规则区，用户定义代码区
        (define, rule, user) = content.split('%%')

        # 定义区数据读取
        precedence = []
        define = define.replace('\t', ' ')
        defines = [d for d in define.split('\n') if d != '']
        for d in defines:
            ds = d.split()
            ds[0] += '%'
            ds = [dd[1:-1] for dd in ds]
            precedence.append(ds)

        # 规则区数据读取
        grammar_rule = []
        func_code = []
        self.elements = set()
        rules = [r for r in rule.split('\n') if r != '']
        sum_len = len(rules)
        i = 0
        flag = True

        while i < sum_len:
            left_rule = ''
            rule = rules[i].split()
            while rule[0] != ';':
                if left_rule == '':
                    left_rule = rule[0]
                    self.elements.add(left_rule)
                    ## 第一个为起始S
                    if flag:
                        self.start = left_rule
                        flag = False

                for ii in xrange(len(rule)):
                    if rule[ii][0] == "'" and rule[ii][-1] == "'":
                        rule[ii] = rule[ii][1:-1]
                # if rule[-2].find("'")

                if rule[0] == '|':
                    if rule[-1] == '{':
                        grammar_rule.append([left_rule, rule[1:-1]])
                    else:
                        grammar_rule.append([left_rule, rule[1:]])
                else:
                    if rule[-1] == '{':
                        grammar_rule.append([left_rule, rule[2:-1]])
                    else:
                        grammar_rule.append([left_rule, rule[2:]])

                code = ''
                if rule[-1] == '{':
                    i += 1
                    while rules[i].replace(' ', '').replace('\t', '').replace('}', '') != '':
                        code += rules[i] + '\n'
                        i += 1
                func_code.append(code)
                i += 1
                rule = rules[i].split()

            i += 1

        self.grammar_rule = grammar_rule
        print grammar_rule

        self.func_code = func_code
        self.precedence = precedence
        self.elements = list(self.elements) + self.terminals
        self.elements.append('epsilon')
        self.terminals.append('epsilon')

        print u'yacc数据读取完成，正在进行LR(1)分析以及PPT的生成...'
        self.createLR()
        # 用户定义代码区
        pass

    # 进行LR1分析
    def createLR(self):

        func_rule = []
        for i in xrange(len(self.func_code)):
            code = self.func_code[i]
            if code == '':
                func_rule.append(None)
                continue
            code = 'def func_%d(p):\n' % i + code
            exec code
            func_rule.append(eval('func_%d' % i))

        self.lr1 = LR1(self.grammar_rule, self.precedence, self.elements, self.terminals, self.start, func_rule)

    def feedTokens(self, tokens):
        self.lr1.feedTokens(tokens)
        self.lr1.draw()
