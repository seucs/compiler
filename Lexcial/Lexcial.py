#coding=utf8
from lexeme import Lex

def CheckChar(s):
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
        try:
            dic = {}
            dic[Lex[s]] = s
            LexmeArr.append(dic)
        except KeyError:
            print 'error!!! Can\'t identity the word %s' %s
        mode = 0
    return mode


code = open('..//code//test.cpp','r').read()
LexmeArr = []
mode = 0 # 1->变量名, 2->数字, 3-> 字符串, 4->字符
string = ''
number = ''
variety = ''
character = ''
for s in code:
    #print s
    if mode == 0:
        mode = CheckChar(s)
    elif mode == 1:
        if s in "qwertyuiopasdfghjklzxcvbnm_0123456789":
            variety += s
        else:
            dic = {}
            dic[Lex['variety']] = variety
            LexmeArr.append(dic)
            mode = CheckChar(s)
    elif mode == 2:
        if s in "0123456789":
            number += s
        else:
            dic = {}
            dic[Lex['number']] = number
            LexmeArr.append(dic)
            mode = CheckChar(s)
    elif mode == 3:
        if s != '"':
            string += s
        else:
            string += s
            dic = {}
            dic[Lex['string']] = string
            LexmeArr.append(dic) 
    elif mode == 4:
        if s != '\'':
            character += s
        else:
            string += s
            dic = {}
            dic[Lex['character']] = character
            LexmeArr.append(dic)

print LexmeArr
                  