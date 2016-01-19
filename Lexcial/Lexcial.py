#coding=utf8
from lexeme import Lex

# 全局变量
string = ''
number = ''
variety = ''
character = ''
LexmeArr = []

def CheckChar(s, s2):
    global string,number,variety,character
    mode = 0
    if s in "qwertyuiopasdfghjklzxcvbnm_":
        mode = 1
        variety = s
    elif s in "0123456789":
        mode = 2
        number = s
    elif s == '"':
        mode = 3
        string = s
    elif s == '\'':
        mode = 4
        character = s
    elif s == ' ' or s == '\n' or s == '\t':
        mode = 0
    else:
        dic = {}
        try:
            if s2 == '=':
                i=1
            dic[Lex[s+s2]] = s+s2
            LexmeArr.append(dic)
            mode = -1
        except KeyError:
            try:
                dic[Lex[s]] = s
                LexmeArr.append(dic)
            except KeyError:
                print 'error!!! Can\'t identity the word %s' %s
            mode = 0
    return mode

def Lexcial():
    global string,number,variety,character
    code = open('..//code//test.cpp','r').read()
    mode = 0 # -1->跳过，0->特殊字符，1->变量名, 2->数字, 3-> 字符串, 4->字符
    string = ''
    number = ''
    variety = ''
    character = ''

    for i in range(len(code)):
        #print s
        s = code[i]
        s2 = ''
        if i < len(code) - 1:
            s2 = code[i+1]
        if mode == -1:
            mode = 0
        elif mode == 0:
            mode = CheckChar(s, s2)
        elif mode == 1:
            if s in "qwertyuiopasdfghjklzxcvbnm_0123456789":
                variety += s
            else:
                dic = {}
                dic[Lex['variety']] = variety
                LexmeArr.append(dic)
                mode = CheckChar(s, s2)
        elif mode == 2:
            if s in "0123456789":
                number += s
            else:
                dic = {}
                dic[Lex['number']] = number
                LexmeArr.append(dic)
                mode = CheckChar(s, s2)
        elif mode == 3:
            if s != '"':
                string += s
            else:
                string += s
                dic = {}
                dic[Lex['string']] = string
                LexmeArr.append(dic) 
                mode = 0
        elif mode == 4:
            if s != '\'':
                character += s
            else:
                string += s
                dic = {}
                dic[Lex['character']] = character
                LexmeArr.append(dic)
                mode = 0

Lexcial()
for item in LexmeArr:
    print item

                  