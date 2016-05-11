#coding=utf8
# 规定-1为空，-2为$
from other import Stack

Syn = {
    'E':[['T','E1']],
    'E1':[[0,'T','E1'],[-1]],
    'T':[['F','T1']],
    'T1':[[1,'F','T1'],[-1]],
    'F':[[2,'E',3],[4]]
    }

VN = ['E','E1','T','T1','F']
VT = [-2,0,1,2,3,4]

FOLLOW = {}
PPT = {}

# 两个集合合并(不包括空集)
def mergeSet(x,y):
    change_flag = False
    for item in y:
        if (item not in x) and (item != -1):
            change_flag = True
            x.append(item)
    return change_flag

# 集合添加元素
def addSet(x,a):
    change_flag = False
    if a not in x:
        x.append(a)
        change_flag = True
    return change_flag

# 判断是否为终结符
def isTerminal(x):
    return type(x) == int

# 求单个符号的FIRST集
def FIRST(x):
    first = []
    if isTerminal(x):
        first.append(x)
        return first
    else:
        for rule in Syn[x]:
            blank_flag = True
            for y in rule:
                Fy = FIRST(y)
                mergeSet(first,Fy)
                if -1 not in Fy:  
                    blank_flag = False              
                    break
                else:
                    continue
            if blank_flag:
                addSet(first,-1)
    return first

# 求一串符号的FIRST集
def strFIRST(arr):
    first = []
    blank_flag = True
    for item in arr:
        Fi = FIRST(item)
        mergeSet(first,Fi)
        if -1 not in Fi:
            blank_flag = False
            break
        else:
            continue
    if blank_flag:
        addSet(first,-1)
    return first

# 求全部非终结符的FOLLOW集
def allFOLLOW(S):
    for k in Syn:
        FOLLOW[k] = []
    FOLLOW[S].append(-2)

    change_flag = True
    while change_flag:
        change_flag = False
        for Tn,rules in Syn.iteritems():
            for rule in rules:
                count = len(rule)
                for i in range(count):
                    if isTerminal(rule[i]):
                        continue
                    beta = []
                    if i != count:
                        for j in range(i+1,count):
                            beta.append(rule[j])
                    Fb = strFIRST(beta)
                    change_flag = mergeSet(FOLLOW[rule[i]], Fb)
                    if -1 in Fb or beta == []:
                        change_flag = mergeSet(FOLLOW[rule[i]],FOLLOW[Tn])

# 生成预测分析表
def createPPT(S):
    allFOLLOW(S)
    for vn in VN:
        PPT[vn] = {}
        for vt in VT:
             PPT[vn][vt] = []

    for Tn,rules in Syn.iteritems():
        for rule in rules:
            Fb = strFIRST(rule)
            for vt in Fb:
                if vt == -1:
                    continue
                PPT[Tn][vt] = rule
            
            
            if -1 in Fb:
                for vt in FOLLOW[Tn]:
                    PPT[Tn][vt] = rule

# 分析输入的Token序列
def parserStr(S,Tokenstr):
    Tokenstr.append(-2)
    sta = Stack()
    sta.push(S)
    parser = {
    'parserStack':[],
    'lastString':[],
    'production':[]
    }
    i = 0

    for s in Tokenstr:
        while True:
            parser['parserStack'].append(str(sta.stack))
            parser['lastString'].append(Tokenstr[i:])
            if sta.isEmpty():
                break
            if sta._top() == s:
                sta.pop()
                parser['production'].append(str([]))
                break
            rule = PPT[sta._top()][s]
            if rule == []:
                print 'error!!!!!!!!!!!!!!!!!'
                return parser
                break
            parser['production'].append(str(rule))
            sta.pop()
            for item in rule[::-1]:
                if item == -1:
                    continue
                sta.push(item)
        i += 1
    parser['production'].append(str(['accept']))
    return parser        
        
createPPT('E')
p = parserStr('E',[4,0,4,1])

l = len(p['production'])
print '%-30s%-30s%-30s' %('parserStack','lastString','production')
for i in range(l):
    print '%-30s%-30s%-30s' %(p['parserStack'][i],p['lastString'][i],p['production'][i])
