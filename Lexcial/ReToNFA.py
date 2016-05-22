# -*- coding: utf-8 -*-
# RegEx -> NFA
# Created by Shengjia Yan @2016-5-21
import networkx as nx
import matplotlib.pyplot as plt
import pydot

class NFA:
    def __init__(self):
        self.graph = nx.MultiDiGraph()    # 构建有向图
        self.first = -1       # 起点
        self.last  = -1       # 终点
        self.lastArr = {}
        
    def __str__(self):
        return str(self.first) + '--' + str(self.graph[self.first]) + '--' + str(self.last)

    # 将 nfa 存储成 .dot 文件
    def storeAsDot(self, name='nfa'):
        nx.write_dot(self.graph, name + '.dot')      
        g = pydot.graph_from_dot_file(name+'.dot')
        g.write_jpg(name+'.jpg')

    # 获取info信息
    def getInfo(self):
        res = {}
        res['start'] = self.first
        res['end'] = self.lastArr
        edge = []
        for k,v in self.dic.iteritems():
            for k2 in v.keys():
                edge.append(k2)
        edge = set(edge)
        edge.remove('epsilon')
        edge = list(edge)
        
        res['edge'] = edge
        
        return res

    # 将 nfa 存储为 dict格式
    def graph2dict(self):
        self.dic = {}
        for node, nbrsdict in self.graph.adjacency_iter():
            EDGE = {}
            NBR = []
            for nbr, attr in nbrsdict.iteritems():
                try:
                    EDGE[attr[0]['label']].append(nbr)
                except:
                    EDGE[attr[0]['label']] = [nbr]
            self.dic[node] = EDGE

    def store(self, property):
        self.storeAsDot()
        self.graph2dict()
        self.property = property
        self.lastArr[self.last] = property

    def refresh(self):
        self.storeAsDot()
        self.graph2dict()

    
class NFAManager:
    def __init__(self):
        self.next_node = -1

    def feed(self, re, property):
        #self.next_node = -1
        re = self.convertSquareBrackets(re)
        nfa = self.convert(re)
        nfa.store(property)
        return nfa

    # 增加节点
    def nextNode(self):
        self.next_node += 1
        return self.next_node

    # 处理方括号[]，将方括号中的内容转成『或』的形式
    def convertSquareBrackets(self, string):
        i = 0
        small = ''
        big = ''
        m = 0
        n = 0
        newstr = ""
        flag = False    # 是否进入方括号内
        while i != len(string):
            if string[i] == '[':
                newstr += '('
                flag = True
            elif string[i] == ']':
                newstr += ')'
                flag = False
            elif string[i] == '-':    # 必然出现在方括号内
                small = string[i-1]
                big = string[i+1]
                m = ord(small)
                n = ord(big)
                for j in range(m, n+1):
                    if j == n and string[i+2] == ']':
                        newstr += chr(j)
                    else:
                        newstr += chr(j)
                        newstr += "|"
            else:
                if flag == False:   # 方括号外
                    newstr += string[i]
                if flag == True:    # 方括号内
                    if string[i-1] != '-' and string[i+1] != '-':
                        if string[i+1] == ']':
                            newstr += string[i]
                        else:
                            newstr += string[i]
                            newstr += '|'
            i += 1
        return newstr

    # 将 RegEx 转换成 NFA
    def convert(self, input_str):
        
        # 处理圆括号()，返回右圆括号)的位置
        def findParenthesis(string, pos):
            temp = -1
            i = pos
            while i != len(string) and temp != 0:
                if string[i] == '(':
                    temp -= 1
                if string[i] == ')':
                    temp += 1
                    if temp == 0:
                        return i
                i += 1

    
        # 将终结符转换为NFA
        def convertTerminal2NFA(terminal):
            mg = NFA()
            mg.first = self.nextNode()
            mg.last = self.nextNode()
            mg.graph.add_edge(mg.first, mg.last, label=terminal)
            return mg

        # 重复
        def repeat(mg):
            first_nexts = [(i, mg.graph[mg.first][i][0]['label']) for i in mg.graph[mg.first]]
            for n, v in first_nexts:
                mg.graph.add_edge(mg.last, n, label=v)
            mg.graph.remove_node(mg.first)
            mg.first = mg.last
            return mg

        # 串联
        def concat(mg1, mg2):
            mg1.graph = nx.union(mg1.graph, mg2.graph)
            mg1.graph.add_edge(mg1.last, mg2.first, label='epsilon')
            mg1.last  = mg2.last
            return mg1

        # 控制符
        def controlSymbols():
            return ['(', ')', '*', '|']

        # 是控制符？
        def isControlSymbol(char):
            return char in controlSymbols()

        # 是终结符？
        def isTerminalSymbol(char):
            return not char in controlSymbols()

        # 获取所有终结符
        def getAllTerminals(re):
            return set([char for char in re if isTerminalSymbol(char)])

        #############主程序##################
        length = len(input_str)
        if length == 0:
            return False

        mg_stack = []
        i = 0

        while i < length:
            char = input_str[i]
            if isControlSymbol(char):   # 是控制符
                if char == '(':
                    pos = findParenthesis(input_str, i + 1)
                    sub_mg = self.convert(input_str[i + 1 : pos])
                    mg_stack.append(sub_mg)
                    i = pos + 1
                if char == '*':
                    prev = mg_stack.pop()
                    sub_mg = repeat(prev)
                    mg_stack.append(sub_mg)
                    i += 1
                if char == '|':
                    mg_stack.append(char)
                    i += 1
            elif isTerminalSymbol(char):
                mg_stack.append(convertTerminal2NFA(char))
                i += 1

        ret_mg = NFA()
        ret_mg.first = self.nextNode()
        ret_mg.last = self.nextNode()
        ret_mg.graph.add_nodes_from([ret_mg.first, ret_mg.last])

        prev = None
        for now in mg_stack:
            if now == '|':
                self.union(ret_mg, prev)
                prev = None
            else:
                if prev is not None:
                    prev = concat(prev, now)
                else:
                    prev = now
        if prev is not None:
            self.union(ret_mg, prev)
        return ret_mg

    # 合并
    def union(self, nfa1, nfa2):
        nfa1.graph = nx.union(nfa1.graph, nfa2.graph)
        nfa1.graph.add_edge(nfa1.first, nfa2.first, label='epsilon')
        nfa1.graph.add_edge(nfa2.last, nfa1.last, label='epsilon')
        return nfa1

    # 连接nfa
    # 注意必须一直把第一个放在最前面
    def mergeNFA(self, nfa1, nfa2):
        nfa1.graph = nx.union(nfa1.graph, nfa2.graph)
        nfa1.graph.add_edge(nfa1.first, nfa2.first, label='epsilon')
        #nfa1.graph.add_edge(nfa2.last, nfa1.last, label='epsilon')
        nfa1.lastArr[nfa2.last] = nfa2.property
        nfa1.refresh()
        return nfa1

    # 输入一串nfa，输出合并后的nfa
    def merge(self, nfaArr):
        nfa = nfaArr[0]
        for i in xrange(1, len(nfaArr)):
            nfa = self.mergeNFA(nfa, nfaArr[i])
        return nfa

#nfaManager = NFAManager()
#nfa1 = nfaManager.feed('[a-z][a-z]*','1')
#nfa2 = nfaManager.feed('4|5','2')
#nfa = nfaManager.mergeNFA(nfa1, nfa2)
#print nfa.dic