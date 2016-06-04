# -*- coding: utf-8 -*-
# LR 总控程序(查表程序)
# Created by Shengjia Yan@2016-5-30


# 带 epsilon 的表达式文法
grammar_rule = [
    ['statement', ['NAME', '=', 'expression']],          
    ['statement', ['expression']],                       
    ['expression', ['expression', '+', 'expression']], 
    ['expression', ['expression', '-', 'expression']],
    ['expression', ['expression', '*', 'expression']],
    ['expression', ['expression', '/', 'expression']],        
    ['expression', ['-', 'expression'], '%prec UMINUS'],     
    ### 这里标记着 %prec UMINUS，意思是规约成这种情况时结合优先级同UMINUS   即-1-3这种情况是(-1)-3而不是-(1-3)
    ### 暂时以这种方式给出，即数组的第三个位置                
    ['expression', ['(', 'expression', ')']],           
    ['expression', ['NUMBER']],
    ['expression', ['NAME']],
]


def func_0(p):
    pass
def func_1(p):
    pass
def func_2(p):
    p[0] = p[1] + p[3]
def func_3(p):
    p[0] = p[1] - p[3]
def func_4(p):
    p[0] = p[1] * p[3]
def func_5(p):
    p[0] = p[1] / p[3]
def func_6(p):
    p[0] = - p[1]
def func_7(p):
    p[0] = p[2]
def func_8(p):
    p[0] = p[1]
def func_9(p):
    pass

func_rule = [func_0, func_1, func_2, func_3, func_4, func_5,func_6,func_7,func_8, func_9]




# 带 epsilon 的 LR分析表
parsing_table = {
0 : {'ACTION': {'(': 'S15', '-': 'S13', 'NAME': 'S33', 'NUMBER': 'S12'}, 'GOTO': {'expression': 2, 'statement': 1}},
1 : {'ACTION': {'$': 'acc'}, 'GOTO': {}},
2 : {'ACTION': {'+': 'S3', '*': 'S7', '-': 'S5', '$': 'r1', '/': 'S9'}, 'GOTO': {}},
3 : {'ACTION': {'(': 'S15', '-': 'S13', 'NAME': 'S11', 'NUMBER': 'S12'}, 'GOTO': {'expression': 4}},
4 : {'ACTION': {'+': 'S3', '*': 'S7', '-': 'S5', '$': 'r2', '/': 'S9'}, 'GOTO': {}},
5 : {'ACTION': {'(': 'S15', '-': 'S13', 'NAME': 'S11', 'NUMBER': 'S12'}, 'GOTO': {'expression': 6}},
6 : {'ACTION': {'+': 'S3', '*': 'S7', '-': 'S5', '$': 'r3', '/': 'S9'}, 'GOTO': {}},
7 : {'ACTION': {'(': 'S15', '-': 'S13', 'NAME': 'S11', 'NUMBER': 'S12'}, 'GOTO': {'expression': 8}},
8 : {'ACTION': {'+': 'r4', '*': 'S7', '-': 'r4', '$': 'r4', '/': 'S9'}, 'GOTO': {}},
9 : {'ACTION': {'(': 'S15', '-': 'S13', 'NAME': 'S11', 'NUMBER': 'S12'}, 'GOTO': {'expression': 10}},
10 : {'ACTION': {'+': 'r5', '*': 'S7', '-': 'r5', '$': 'r5', '/': 'S9'}, 'GOTO': {}},
11 : {'ACTION': {'+': 'r9', '*': 'r9', '-': 'r9', '$': 'r9', '/': 'r9'}, 'GOTO': {}},
12 : {'ACTION': {'+': 'r8', '*': 'r8', '-': 'r8', '$': 'r8', '/': 'r8'}, 'GOTO': {}},
13 : {'ACTION': {'(': 'S15', '-': 'S13', 'NAME': 'S11', 'NUMBER': 'S12'}, 'GOTO': {'expression': 14}},
14 : {'ACTION': {'+': 'S3', '*': 'S7', '-': 'S5', '$': 'r6', '/': 'S9'}, 'GOTO': {}},
15 : {'ACTION': {'(': 'S29', '-': 'S27', 'NAME': 'S25', 'NUMBER': 'S26'}, 'GOTO': {'expression': 16}},
16 : {'ACTION': {')': 'S32', '+': 'S17', '*': 'S21', '-': 'S19', '/': 'S23'}, 'GOTO': {}},
17 : {'ACTION': {'(': 'S29', '-': 'S27', 'NAME': 'S25', 'NUMBER': 'S26'}, 'GOTO': {'expression': 18}},
18 : {'ACTION': {'$': 'r2', ')': 'r2', '+': 'S17', '*': 'S21', '-': 'S19', '/': 'S23'}, 'GOTO': {}},
19 : {'ACTION': {'(': 'S29', '-': 'S27', 'NAME': 'S25', 'NUMBER': 'S26'}, 'GOTO': {'expression': 20}},
20 : {'ACTION': {'$': 'r3', ')': 'r3', '+': 'S17', '*': 'S21', '-': 'S19', '/': 'S23'}, 'GOTO': {}},
21 : {'ACTION': {'(': 'S29', '-': 'S27', 'NAME': 'S25', 'NUMBER': 'S26'}, 'GOTO': {'expression': 22}},
22 : {'ACTION': {'$': 'r4', ')': 'r4', '+': 'r4', '*': 'S21', '-': 'r4', '/': 'S23'}, 'GOTO': {}},
23 : {'ACTION': {'(': 'S29', '-': 'S27', 'NAME': 'S25', 'NUMBER': 'S26'}, 'GOTO': {'expression': 24}},
24 : {'ACTION': {'$': 'r5', ')': 'r5', '+': 'r5', '*': 'S21', '-': 'r5', '/': 'S23'}, 'GOTO': {}},
25 : {'ACTION': {'$': 'r9', ')': 'r9', '+': 'r9', '*': 'r9', '-': 'r9', '/': 'r9'}, 'GOTO': {}},
26 : {'ACTION': {'$': 'r8', ')': 'r8', '+': 'r8', '*': 'r8', '-': 'r8', '/': 'r8'}, 'GOTO': {}},
27 : {'ACTION': {'(': 'S29', '-': 'S27', 'NAME': 'S25', 'NUMBER': 'S26'}, 'GOTO': {'expression': 28}},
28 : {'ACTION': {'$': 'r6', ')': 'r6', '+': 'S17', '*': 'S21', '-': 'S19', '/': 'S23'}, 'GOTO': {}},
29 : {'ACTION': {'(': 'S29', '-': 'S27', 'NAME': 'S25', 'NUMBER': 'S26'}, 'GOTO': {'expression': 30}},
30 : {'ACTION': {')': 'S31', '+': 'S17', '*': 'S21', '-': 'S19', '/': 'S23'}, 'GOTO': {}},
31 : {'ACTION': {'$': 'r7', ')': 'r7', '+': 'r7', '*': 'r7', '-': 'r7', '/': 'r7'}, 'GOTO': {}},
32 : {'ACTION': {'+': 'r7', '*': 'r7', '-': 'r7', '$': 'r7', '/': 'r7'}, 'GOTO': {}},
33 : {'ACTION': {'+': 'r9', '*': 'r9', '-': 'r9', '$': 'r-1', '/': 'r9'}, 'GOTO': {'statement': 34}},
34 : {'ACTION': {}, 'GOTO': {}}
}



# 终结符
def terminalSymbols():
    return ['i', '+', '*', '(', ')', '#']

# 非终结符
def nonTerminalSymbols():
    return ['E', 'T', 'F']

# 是终结符？
def isTerminalSymbol(char):
    return char in terminalSymbols()

# 是非终结符？
def isNonTerminalSymbols(char):
    return char in nonTerminalSymbols()


class Token():
    def __init__(self, name, value=''):
        self.name = name
        if value == '':
            self.value = name
        else:
            self.value = value

# 总控程序
def allControl(input_stack): # 输入栈 Token型   
    state_stack  = []        # 状态栈 整型
    symbol_stack = []        # 符号栈 字符串型
    value_stack  = []        # 值栈   整型或字符串型
    pointer      = 0         # 输入串的读头
    move         = ""        # 总控程序的动作

    state_stack.append(0)             # 状态栈的初始状态为0
    symbol_stack.append('$')   # 符号栈的栈底符为 $
    input_stack.append(Token('$'))    # 输入Token栈以 $ 结尾

    print "%-30s%-30s%-30s%-30s%-30s" %("State Stack", "Symbol Stack", "Input Token", "Value Stack", "Move")

    # 开始分析输入串，总控程序每做一个动作循环一次
    while 1:
        state_string  = ' '.join(map(str, state_stack))                                          # 状态栈转成字符串
        symbol_string = ' '.join(symbol_stack)                                                   # 符号栈转成字符串
        input_string  = ' '.join(input_stack[i].name for i in range(pointer, len(input_stack)))  # 输入Token栈转成字符串
        value_string  = ''
        for i in range(len(value_stack)):
            value_string += str(value_stack[i])
        print "%-30s%-30s%-30s%-30s%-30s" %(state_string, symbol_string, input_string, value_string, move)

        input_token = input_stack[pointer]       # 当前读入符，应该是一个终结符
        input_token_name = input_token.name
        current_state = state_stack[-1]          # 当前状态为状态栈栈顶元素


        # 遇到 ACTION 表中空白格，跳转到 epsilon 列或报错
        if parsing_table[current_state]['ACTION'].has_key(input_token_name) == False:
            # 转到 ACTION 表中 epsilon 列
            if parsing_table[current_state]['ACTION'].has_key('epsilon') == False:  # 当前状态行没有 epsilon 动作
                print 'error'
                break
            else:   # 当前状态行有 epsilon 动作
                symbol_in_table = parsing_table[current_state]['ACTION']['epsilon']       # 表中符号

                # 遇到 'acc'，分析成功
                if symbol_in_table == 'acc':
                    print 'Analyse Successfully!'
                    break

                action = symbol_in_table[0]          # Shift or Reduce
                number = int(symbol_in_table[1:])    # 'S' 或 'r' 后的数字

                # Shift
                if action == 'S':
                    state_stack.append(number)              # 移进的目标状态压入状态栈
                    symbol_stack.append('epsilon')   # 当前读入符压入符号栈
                    value_stack.append(input_token.value)   # 当前读入符的值压入值栈
                    move = symbol_in_table + " Shift"       # 当前动作为『移进』
                                                            # 读头不动

                reduce_error = True     # 产生式是否有错

                # Reduce
                if action == 'r':
                    len_production = len(grammar_rule[number])         # 符号栈按照 产生式[number] 归约

                    # 遍历产生式右部用'|'分割开的部分，寻找适合归约的产生式右部
                    for i in range(1, len_production):
                        len_right = len(grammar_rule[number][i])     # 归约产生式第 i 个右部的长度
                        len_symbol = len(symbol_stack)               # 符号栈的长度

                        # 避免数组越界
                        if len_right > (len_symbol-1):
                            continue
                        else:
                            temp_production_right = ''.join(grammar_rule[number][i])         # 归约产生式第 i 个右部转成字符串
                            temp_symbol_string    = ''.join(symbol_stack[-len_right:])  # 符号栈最后 len_right 个元素转成字符串

                            if temp_production_right in temp_symbol_string:        # 用于归约的产生式右部
                                reduce_error = False                               # 产生式没有错误
                                production_left  = grammar_rule[number][0]         # 归约产生式的左部列表
                                production_right = grammar_rule[number][i]         # 归约产生式的右部列表

                                len_right = len(production_right)                  # 产生式右部的长度

                                p = []
                                p.append(0)

                                # 弹出栈顶的 len_right 项
                                for j in range(len_right):
                                    symbol_stack.pop()
                                    state_stack.pop()
                                    temp_value = value_stack.pop()
                                    p.append(temp_value)

                                # 语义动作 p[0]保存当前归约产生式运算后的结果
                                func_rule[number](p)

                                symbol_stack.append(production_left)     # 将产生式左部和对应的值压入符号栈中
                                value_stack.append(p[0])                 # 归约完的值压入值栈
                                temp_current_state = state_stack[-1]     # 当前状态为状态栈栈顶元素

                                # 遇到 GOTO 表中空白格，报错
                                if parsing_table[temp_current_state]['GOTO'].has_key(production_left) == False:
                                    print 'error'
                                    break

                                next_state = parsing_table[temp_current_state]['GOTO'][production_left] # 下一状态
                                state_stack.append(next_state)           # 将下一状态压入状态栈

                                break

                    move = symbol_in_table + " Reduce"       # 当前动作为『归约』

                    if reduce_error == True:
                        print "Production "+ str(number) + " error!"
                        break

                continue

        else:
            symbol_in_table = parsing_table[current_state]['ACTION'][input_token_name]    # 表中符号


        # 遇到 'acc'，分析成功
        if symbol_in_table == 'acc':
            print 'Analyse Successfully!'
            break

        action = symbol_in_table[0]          # Shift or Reduce
        number = int(symbol_in_table[1:])    # 'S' 或 'r' 后的数字

        # Shift
        if action == 'S':
            state_stack.append(number)              # 移进的目标状态压入状态栈
            symbol_stack.append(input_token.name)   # 当前读入符压入符号栈
            value_stack.append(input_token.value)   # 当前读入符的值压入值栈
            move = symbol_in_table + " Shift"       # 当前动作为『移进』
            pointer += 1                            # 读头前进一格

        reduce_error = True     # 产生式是否有错

        # Reduce
        if action == 'r':
            len_production = len(grammar_rule[number])         # 符号栈按照 产生式[number] 归约

            # 遍历产生式右部用'|'分割开的部分，寻找适合归约的产生式右部
            for i in range(1, len_production):
                len_right = len(grammar_rule[number][i])     # 归约产生式第 i 个右部的长度
                len_symbol = len(symbol_stack)               # 符号栈的长度

                # 避免数组越界
                if len_right > (len_symbol-1):
                    continue
                else:
                    temp_production_right = ''.join(grammar_rule[number][i])         # 归约产生式第 i 个右部转成字符串
                    temp_symbol_string    = ''.join(symbol_stack[-len_right:])  # 符号栈最后 len_right 个元素转成字符串

                    if temp_production_right in temp_symbol_string:        # 用于归约的产生式右部
                        reduce_error = False                               # 产生式没有错误
                        production_left  = grammar_rule[number][0]         # 归约产生式的左部列表
                        production_right = grammar_rule[number][i]         # 归约产生式的右部列表

                        len_right = len(production_right)                  # 产生式右部的长度

                        p = []
                        p.append(0)

                        # 弹出栈顶的 len_right 项
                        for j in range(len_right):
                            symbol_stack.pop()
                            state_stack.pop()
                            temp_value = value_stack.pop()
                            p.append(temp_value)

                        # 语义动作 p[0]保存当前归约产生式运算后的结果
                        func_rule[number](p)

                        symbol_stack.append(production_left)     # 将产生式左部和对应的值压入符号栈中
                        value_stack.append(p[0])                 # 归约完的值压入值栈
                        temp_current_state = state_stack[-1]     # 当前状态为状态栈栈顶元素

                        # 遇到 GOTO 表中空白格，报错
                        if parsing_table[temp_current_state]['GOTO'].has_key(production_left) == False:
                            print 'error'
                            break

                        next_state = parsing_table[temp_current_state]['GOTO'][production_left] # 下一状态
                        state_stack.append(next_state)           # 将下一状态压入状态栈

                        break

            move = symbol_in_table + " Reduce"       # 当前动作为『归约』

            if reduce_error == True:
                print "Production "+ str(number) + " error!"
                break



if __name__ == "__main__":
    # TokenArr = [Token('number',2), Token('*'), Token('number',2), Token('+'), Token('number',3)]
    TokenArr = [Token('NUMBER',2), Token('+'),Token('NUMBER',3),Token('*'), Token('NUMBER',4)]
    allControl(TokenArr)
