#coding=utf8
import new
import sys
import re as libre
from ReToNFA import NFA, NFAManager
from NFAtoDFA import DFAmanager
reload(sys)
sys.setdefaultencoding('utf8')

class Re_Token():
    def __init__(self, lexer, re):
        self.lexer = lexer
        self.func = None
        self.re = re
        self.name = re

    def extends(self):
        if self.func != None:
            func = 'def callBack(self):\n' 
            for code in self.func.split('\n'):
                func+='\t'+code+'\n'
            exec func + '_method = callBack'
            self.__dict__['callBack'] = new.instancemethod(_method,self,None)
            self.callBack()	

class Token():
    def __init__(self, name, value = ''):
        self.name = name
        if value == '':
            self.value = name
        else:
            self.value = value

class Lex():

    # 初始化
    def __init__(self, path):
        self.lineno = 0
        self.keywords = {}
        with open(path,'r') as f:
            self.parserLexFile(f.read())
    
    # 读取lex文件信息
    def parserLexFile(self, content):
        #定义区，规则区，用户定义代码区
        (define, rule, user) = content.split('%%')

        # 定义区数据读取
        temp_token = {}
        define = define.replace('\t',' ')
        defines = [d for d in define.split('\n') if d != '']
        for d in defines:
            token_name = d[:d.index(' ')]
            token_re = d[d.index('['):d.rindex(']')+1]
            temp_token[token_name] = token_re

        
        # 规则区数据读取
        tokenArr = self.ReTokenArr = []
        rules = [r for r in rule.split('\n') if r != '']
        code_flag = False
        code = ''
        cur_Token = None
        for r in rules:
            #print r
            if code_flag:
                if r.find('}') != -1:
                    code_flag = False
                    cur_Token.func = code[:-1]
                    tokenArr.append(cur_Token)
                    code = ''
                else:
                    code += r.strip() + '\n'
            elif r.find('"') != -1:
                token_re = r[r.index('"')+1:r.rindex('"')]
                tokenArr.append(Re_Token(self, token_re))
            elif r.find('{') == -1:
                token_re = r.strip()
                tokenArr.append(Re_Token(self, token_re))
            else:
                token_re = r[:r.rindex('{')].strip()
                cur_Token = Re_Token(self, token_re)
                code_flag = True

        # 替换定义区正规表达式
        for token in tokenArr:
            for k,v in temp_token.iteritems():
                    token.re = token.re.replace('{'+k+'}',v)
            token.extends()

        print u'lex数据读取完成，正在进行Re->NFA'
        self.ReToNFA()
        # 用户定义代码区
        pass

    # 解析正规表达式
    def ReToNFA(self):
        nfaManager = NFAManager()
        nfaArr = []
        for token in self.ReTokenArr:
            token.re =  token.re.replace('\\n','\n').replace('\\t','\t').replace('\\r','\r')
            if token.re == '(' or token.re == ')' or token.re == '*':
                token.re = "\\" + token.re
            #print token.re
            if libre.match(r'[a-z]+',token.re):
                self.keywords[token.re] = token.re
            else:
                nfaArr.append(nfaManager.feed(token.re,token.name))
        self.nfa = nfaManager.merge(nfaArr)

        print u'Re->NFA完成，正在执行NFA->DFA'
        self.NFAtoDFA()
        
    def NFAtoDFA(self):
        nfa = self.nfa
        self.dfacreator = DFAmanager(nfa.dic,nfa.getInfo())
        self.dfacreator.creatDFA()
        self.dfacreator.draw()
        print u'NFA->DFA完成，正在读取数据'

    def feedCode(self, code_path):  
        with open(code_path,'r') as f:
            res = self.dfacreator.judgeString(f.read(), self.keywords)
           

        TokenArr = []
        for r in res:
            if r['category'] == 'IGNORE':
                continue
            print r
            if r['category'] == 'NUMBER':
                TokenArr.append(Token(r['category'], int(r['mention'])))
            else:
                TokenArr.append(Token(r['category'], r['mention']))

        return TokenArr

    def getTerminals(self):
        terminals = []
        for s in self.ReTokenArr:
            if s.name == 'IGNORE':
                continue
            terminals.append(s.name)

        return terminals

