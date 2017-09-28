# -*- coding: utf-8 -*-
# @Time    : 2016/12/4 下午3:05
# @Author  : Zhixin Piao 
# @Email   : piaozhx@seu.edu.cn

import copy
from seulex import Token
import pydot
import networkx as nx
from networkx.drawing.nx_pydot import to_pydot


class LR1:
    def __init__(self, grammar_rule, precedence, elements, token, start, func_rule):
        self.grammar_rule = grammar_rule
        self.elements = elements
        self.precedence = precedence
        self.token = token
        self.start = start
        self.func_rule = func_rule

        # 主程序部分
        self.create_goto()
        # self.draw()

    def creat_table(self):
        statenum = -1
        for state in self.goto:
            statenum += 1
            for progress in state:
                if progress[1] == len(self.grammar_rule[progress[0]][1]):
                    for endphase in progress[2]:
                        if self.parsing_table[statenum]['ACTION'].has_key(endphase):
                            finaltoken = ''
                            for token in self.grammar_rule[progress[0]][1]:
                                if token in self.token:
                                    finaltoken = token

                            for ii in xrange(len(self.precedence)):
                                if finaltoken in self.precedence[ii]:
                                    final_token_prec = ii
                                if endphase in self.precedence[ii]:
                                    endphase_prec = ii
                            if final_token_prec == endphase_prec:
                                pass
                            elif final_token_prec > endphase_prec:
                                self.parsing_table[statenum]['ACTION'][endphase] = ('r' + str(progress[0]))
                            elif final_token_prec < endphase_prec:
                                pass

                        else:
                            self.parsing_table[statenum]['ACTION'].setdefault(endphase, ('r' + str(progress[0])))
                        if progress[0] == -2:
                            self.parsing_table[statenum]['ACTION'][endphase] = 'acc'
                else:
                    if progress[0] == -2:
                        for endphase in progress[2]:
                            self.parsing_table[statenum]['ACTION'].setdefault(endphase, 'acc')

        self.parsing_table[1]['ACTION'].setdefault('$', 'acc')

    def update_goto(self, gotolist, newstate):
        self.statecounter += 1
        thisnum = self.statecounter  # 记录本次的状态数
        gotolist.append(newstate)
        self.parsing_table.setdefault(self.statecounter, {'ACTION': {}, 'GOTO': {}})
        self.state_present.setdefault(thisnum, {})
        self.progress_present.setdefault(thisnum, [])
        for progress in newstate:
            if progress[0] == -1:
                self.progress_present[thisnum].append([self.start + "'", [self.start]])
            else:
                temppresent = copy.deepcopy(self.grammar_rule[progress[0]])
                temppresent[1].insert(progress[1], "dot")
                self.progress_present[thisnum].append(temppresent)

        for element in self.elements:
            tempstate = []

            for progress in newstate:
                if progress[0] == -1:
                    if element == self.start:
                        tempstate.append([-2, progress[1] + 1, progress[2]])
                if progress[0] == -2:
                    continue

                if progress[1] < len(self.grammar_rule[progress[0]][1]):  # 如果没到头
                    if self.grammar_rule[progress[0]][1][progress[1]] == element:
                        tempstate.append([progress[0], progress[1] + 1, progress[2]])

            for new_progree in tempstate:
                sentence_num = -1
                for sentence in self.grammar_rule:
                    sentence_num += 1
                    tempprogress = []
                    if [new_progree[1]] < len(self.grammar_rule[new_progree[0]][1]):
                        if sentence[0] == self.grammar_rule[new_progree[0]][1][new_progree[1]]:
                            tempprogress = [sentence_num, 0, new_progree[2]]
                            flag = 1
                            for old_progress in tempstate:
                                if old_progress == tempprogress:
                                    flag = 0
                            if flag == 1:
                                tempstate.append(tempprogress)

            self.update_closure(tempstate)

            flag = 1
            oldstatenum = -1
            for state in gotolist:
                oldstatenum += 1
                if state == tempstate:

                    self.state_present[thisnum].setdefault(element, oldstatenum)

                    if element in self.token:
                        self.parsing_table[thisnum]['ACTION'].setdefault(element, "S" + str(oldstatenum))
                    else:
                        self.parsing_table[thisnum]['GOTO'].setdefault(element, oldstatenum)
                    flag = 0
            if len(tempstate) == 0:
                flag = 0
            if flag == 1:
                self.state_present[thisnum].setdefault(element, self.statecounter + 1)
                if element in self.token:
                    self.parsing_table[thisnum]['ACTION'].setdefault(element, "S" + str(self.statecounter + 1))
                else:
                    self.parsing_table[thisnum]['GOTO'].setdefault(element, self.statecounter + 1)
                self.update_goto(gotolist, tempstate)

    def update_start_state(self):
        self.startstate = [[-1, 0, ['$']]]
        sentence_num = -1
        for sentence in self.grammar_rule:
            sentence_num += 1
            if sentence[0] == self.start:
                self.startstate.append([sentence_num, 0, ['$']])

        self.update_closure(self.startstate)

    def update_closure(self, state):
        for sentence in state:
            if sentence[0] != -1:
                if len(self.grammar_rule[sentence[0]][1]) > sentence[1]:
                    if self.grammar_rule[sentence[0]][1][sentence[1]] not in self.token:  # 光标的右侧是非终结符
                        sentence_num = -1
                        for sentence_new in self.grammar_rule:
                            sentence_num += 1
                            if sentence_new[0] == self.grammar_rule[sentence[0]][1][sentence[1]]:  # 找到相对应的非终结符
                                newsentence = [sentence_num, 0, sentence[2]]
                                if len(self.grammar_rule[sentence[0]][1]) > sentence[1] + 1:  # 看光标右边第二字字符
                                    newsentence[2] = list(set(
                                        newsentence[2] + self.arrFIRST(self.grammar_rule[sentence[0]][1],
                                                                       sentence[1] + 1)))

                                # 检测新的状态条目是不是已经在状态里了
                                flag = 1
                                for sentence_j in state:
                                    if sentence_j[0] == newsentence[0] and sentence_j[1] == newsentence[1]:
                                        sentence_j[2] = list(set(sentence_j[2] + newsentence[2]))
                                        flag = 0
                                if flag == 1:
                                    state.append(newsentence)
                                    self.update_closure(state)

    def create_goto(self):
        self.goto = []
        state_first = []
        self.update_start_state()
        self.statecounter = -1
        self.parsing_table = {}
        self.state_present = {}
        self.progress_present = {}
        self.update_goto(self.goto, self.startstate)
        self.creat_table()

    # 求一串符号的FIRST集
    def arrFIRST(self, arr, i):
        xx = arr[i:]
        first = set()
        blank_flag = True
        for item in xx:
            Fi = self.FIRST(item)
            first |= Fi
            if 'epsilon' not in Fi:
                blank_flag = False
                break
        if blank_flag:
            first.add('epsilon')
        return list(first)

    # 求单个非终结符的FIRST集
    def FIRST(self, nt):
        first = set()
        if nt in self.token:
            first.add(nt)
            return first

        for m_rule in self.grammar_rule:
            if m_rule[0] != nt:
                continue

            arr = m_rule[1]
            blank_flag = True
            for item in arr:
                Fi = self.FIRST(item)
                first |= Fi
                if 'epsilon' not in Fi:
                    blank_flag = False
                    break
            if blank_flag:
                first.add('epsilon')
        return first

    # 通过PPT分析Token序列
    def feedTokens(self, input_stack):

        func_rule = self.func_rule
        # 需要的数据
        parsing_table = self.parsing_table
        grammar_rule = self.grammar_rule

        state_stack = []  # 状态栈 整型
        symbol_stack = []  # 符号栈 字符串型
        value_stack = []  # 值栈   整型或字符串型
        pointer = 0  # 输入串的读头
        move = ""  # 总控程序的动作

        state_stack.append(0)  # 状态栈的初始状态为0
        symbol_stack.append('$')  # 符号栈的栈底符为 $
        input_stack.append(Token('$'))  # 输入Token栈以 $ 结尾

        print "%-30s%-30s%-30s%-30s%-30s" % ("State Stack", "Symbol Stack", "Input Token", "Value Stack", "Move")

        # 开始分析输入串，总控程序每做一个动作循环一次
        while 1:
            state_string = ' '.join(map(str, state_stack))  # 状态栈转成字符串
            symbol_string = ' '.join(symbol_stack)  # 符号栈转成字符串
            input_string = ' '.join(input_stack[i].name for i in range(pointer, len(input_stack)))  # 输入Token栈转成字符串
            value_string = ''
            for i in range(len(value_stack)):
                value_string += str(value_stack[i])
            # print "%-30s%-30s%-30s%-30s%-30s" %(state_string, symbol_string, input_string, value_string, move)
            print "%-50s%-50s" % (state_string, value_string)

            input_token = input_stack[pointer]  # 当前读入符，应该是一个终结符
            input_token_name = input_token.name
            current_state = state_stack[-1]  # 当前状态为状态栈栈顶元素

            # 遇到 ACTION 表中空白格，跳转到 epsilon 列或报错
            if input_token_name not in parsing_table[current_state]['ACTION']:
                # 转到 ACTION 表中 epsilon 列
                if 'epsilon' not in parsing_table[current_state]['ACTION']:  # 当前状态行没有 epsilon 动作
                    print 'error'
                    break
                else:  # 当前状态行有 epsilon 动作
                    symbol_in_table = parsing_table[current_state]['ACTION']['epsilon']  # 表中符号

                    # 遇到 'acc'，分析成功
                    if symbol_in_table == 'acc':
                        print 'Analyse Successfully!'
                        break

                    action = symbol_in_table[0]  # Shift or Reduce
                    number = int(symbol_in_table[1:])  # 'S' 或 'r' 后的数字

                    # Shift
                    if action == 'S':
                        state_stack.append(number)  # 移进的目标状态压入状态栈
                        symbol_stack.append('epsilon')  # 当前读入符压入符号栈
                        value_stack.append(input_token.value)  # 当前读入符的值压入值栈
                        move = symbol_in_table + " Shift"  # 当前动作为『移进』
                        # 读头不动

                    reduce_error = True  # 产生式是否有错

                    # Reduce
                    if action == 'r':
                        len_production = len(grammar_rule[number])  # 符号栈按照 产生式[number] 归约

                        # 遍历产生式右部用'|'分割开的部分，寻找适合归约的产生式右部
                        for i in range(1, len_production):
                            len_right = len(grammar_rule[number][i])  # 归约产生式第 i 个右部的长度
                            len_symbol = len(symbol_stack)  # 符号栈的长度

                            # 避免数组越界
                            if len_right > (len_symbol - 1):
                                continue
                            else:
                                temp_production_right = ''.join(grammar_rule[number][i])  # 归约产生式第 i 个右部转成字符串
                                temp_symbol_string = ''.join(symbol_stack[-len_right:])  # 符号栈最后 len_right 个元素转成字符串

                                if temp_production_right in temp_symbol_string:  # 用于归约的产生式右部
                                    reduce_error = False  # 产生式没有错误
                                    production_left = grammar_rule[number][0]  # 归约产生式的左部列表
                                    production_right = grammar_rule[number][i]  # 归约产生式的右部列表

                                    len_right = len(production_right)  # 产生式右部的长度

                                    p = [0] * (len_right + 1)

                                    # 弹出栈顶的 len_right 项
                                    temp_p = len_right
                                    for j in range(len_right):
                                        symbol_stack.pop()
                                        state_stack.pop()
                                        temp_value = value_stack.pop()
                                        p[temp_p] = temp_value
                                        temp_p -= 1

                                    # 语义动作 p[0]保存当前归约产生式运算后的结果
                                    if not func_rule[number]:
                                        func_rule[number](p)

                                    symbol_stack.append(production_left)  # 将产生式左部和对应的值压入符号栈中
                                    value_stack.append(p[0])  # 归约完的值压入值栈
                                    temp_current_state = state_stack[-1]  # 当前状态为状态栈栈顶元素

                                    # 遇到 GOTO 表中空白格，报错
                                    if parsing_table[temp_current_state]['GOTO'].has_key(production_left) == False:
                                        print 'error'
                                        break

                                    next_state = parsing_table[temp_current_state]['GOTO'][production_left]  # 下一状态
                                    state_stack.append(next_state)  # 将下一状态压入状态栈

                                    break

                        move = symbol_in_table + " Reduce"  # 当前动作为『归约』

                        if reduce_error:
                            print "Production " + str(number) + " error!"
                            break

                    continue

            else:
                symbol_in_table = parsing_table[current_state]['ACTION'][input_token_name]  # 表中符号

            # 遇到 'acc'，分析成功
            if symbol_in_table == 'acc':
                print 'Analyse Successfully!'
                break

            action = symbol_in_table[0]  # Shift or Reduce
            number = int(symbol_in_table[1:])  # 'S' 或 'r' 后的数字

            # Shift
            if action == 'S':
                state_stack.append(number)  # 移进的目标状态压入状态栈
                symbol_stack.append(input_token.name)  # 当前读入符压入符号栈
                value_stack.append(input_token.value)  # 当前读入符的值压入值栈
                move = symbol_in_table + " Shift"  # 当前动作为『移进』
                pointer += 1  # 读头前进一格

            reduce_error = True  # 产生式是否有错

            # Reduce
            if action == 'r':
                len_production = len(grammar_rule[number])  # 符号栈按照 产生式[number] 归约

                # 遍历产生式右部用'|'分割开的部分，寻找适合归约的产生式右部
                for i in range(1, len_production):
                    len_right = len(grammar_rule[number][i])  # 归约产生式第 i 个右部的长度
                    len_symbol = len(symbol_stack)  # 符号栈的长度

                    # 避免数组越界
                    if len_right > (len_symbol - 1):
                        continue
                    else:
                        temp_production_right = ''.join(grammar_rule[number][i])  # 归约产生式第 i 个右部转成字符串
                        temp_symbol_string = ''.join(symbol_stack[-len_right:])  # 符号栈最后 len_right 个元素转成字符串

                        if temp_production_right in temp_symbol_string:  # 用于归约的产生式右部
                            reduce_error = False  # 产生式没有错误
                            production_left = grammar_rule[number][0]  # 归约产生式的左部列表
                            production_right = grammar_rule[number][i]  # 归约产生式的右部列表

                            len_right = len(production_right)  # 产生式右部的长度

                            p = [0] * (len_right + 1)

                            # 弹出栈顶的 len_right 项
                            temp_p = len_right
                            for j in range(len_right):
                                symbol_stack.pop()
                                state_stack.pop()
                                temp_value = value_stack.pop()
                                p[temp_p] = temp_value
                                temp_p -= 1

                            # 语义动作 p[0]保存当前归约产生式运算后的结果
                            if func_rule[number] is not None:
                                func_rule[number](p)

                            symbol_stack.append(production_left)  # 将产生式左部和对应的值压入符号栈中
                            value_stack.append(p[0])  # 归约完的值压入值栈
                            temp_current_state = state_stack[-1]  # 当前状态为状态栈栈顶元素

                            # 遇到 GOTO 表中空白格，报错
                            if not parsing_table[temp_current_state]['GOTO'].has_key(production_left):
                                print 'error'
                                break

                            next_state = parsing_table[temp_current_state]['GOTO'][production_left]  # 下一状态
                            state_stack.append(next_state)  # 将下一状态压入状态栈

                            break

                move = symbol_in_table + " Reduce"  # 当前动作为『归约』

                if reduce_error:
                    print "Production " + str(number) + " error!"
                    break

    # 通过graghGZ画GOTO图
    def draw(self, name='goto'):
        g = nx.MultiDiGraph()
        lr_content = {}
        for k, v in self.progress_present.iteritems():
            label = 'I %d\n' % k

            for rule in v:
                break
                label += rule[0] + ' --> '
                for r in rule[1]:
                    if r == u'dot':
                        label += '^ '
                    else:
                        label += r + ' '
                label += '\n'
            lr_content[k] = label

        for k, v in self.state_present.iteritems():
            for edge, to in v.iteritems():
                g.add_edge(lr_content[k], lr_content[to], label=edge)

        g_str = to_pydot(g).to_string()
        g = pydot.graph_from_dot_data(g_str)
        g[0].write_jpg('graph/%s.jpg' % name)
        print '%s图生成成功！' % name
