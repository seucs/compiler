#coding=utf8
import new
import json
reload(sys)
sys.setdefaultencoding('utf8')

yacc_path = '../code/minic.cpp'

class Token():
    def __init__(self, name, value = ''):
        self.name = name
        if value == '':
            self.value = name
        else:
            self.value = value


class Yacc():
    def __init__(self, path):
        with open(path,'r') as f:
            self.parserYaccFile(f.read())

    # 读取lex文件信息
    def parserYaccFile(self, content):
        #定义区，规则区，用户定义代码区
        (define, rule, user) = content.split('%%')

        # 定义区数据读取
        precedence = []
        define = define.replace('\t',' ')
        defines = [d for d in define.split('\n') if d != '']
        for d in defines:
            ds = d.split()
            precedence.append((ds[0]))


        
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

        print u'yacc数据读取完成，正在进行'
        self.ReToNFA()
        # 用户定义代码区
        pass

names = []
if_flag = False

yacc = Yacc()
