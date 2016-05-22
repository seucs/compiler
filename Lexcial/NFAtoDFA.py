#coding=utf8
import json
import pydot
import networkx as nx

class DFAmanager:

    def __init__(self,nfa,nfainfo):
        self.NFA_info=nfainfo
        self.NFA = nfa

    def update_closure(self,oldlist,currentlist):
        newlist = []
        for node in currentlist:
            oldlist.append(node)
            for newnode in self.NFA[node]['epsilon']:
                if newnode not in oldlist and newnode not in currentlist and newnode not in newlist:
                    newlist.append(newnode)

        if newlist:
            newlist.sort()
            self.update_closure(oldlist,newlist)
            return
        else:
            return

    def update_DFA(self,currentDFA,newelement,realDFA):
        newelementnum = self.DFAcounter
        currentDFA.setdefault(newelementnum,newelement)
        realDFA.setdefault(newelementnum,{})
        
        

        for edge in self.NFA_info['edge']:

            tempelement =[]
            for node in newelement:    
                for neighbernode in self.NFA[node][edge]:
                    if node == 14 and edge == '4':
                        pass
                        #print neighbernode,'youmuyou'
                    tempelement = list(set(tempelement+self.ee_closure[neighbernode]))

            tempelement.sort()
            elementstate=0
            for (number,element) in currentDFA.iteritems():
                if tempelement==element:
                    elementstate=1
            if elementstate==0 and tempelement:
                if realDFA[newelementnum].has_key(edge):
                    print "DFA ERROR,1 STATE HAVE TWO SAME EDGE!"
                    
                    #if DFAcounter != realDFA[newelementnum][edge]:
                    #    print u"1111111111111111111111111111111节点",newelementnum,":     ",self.DFA_detail[newelementnum],u"通过边",edge,u"已经到达",realDFA[newelementnum][edge],u"不能再链接",DFAcounter
                    #    print "DFA ERROR,1 STATE HAVE TWO SAME EDGE!"
                else:
                    realDFA[newelementnum].setdefault(edge,self.DFAcounter+1)
                self.DFAcounter += 1
                self.update_DFA(currentDFA,tempelement,realDFA)
            else:
                for (node,detail) in currentDFA.iteritems():
                    if detail==tempelement:
                        if realDFA[newelementnum].has_key(edge):
                            if node != realDFA[newelementnum][edge]:
                                print u"节点",newelementnum,":     ",self.DFA_detail[newelementnum],u"通过边",edge,u"已经到达",realDFA[newelementnum][edge],u"不能再链接",node
                                print "DFA ERROR,1 STATE HAVE TWO SAME EDGE!"
                        else:
                            realDFA[newelementnum].setdefault(edge,node)

    def creatDFA(self):
        self.ee_closure ={}
        self.DFA_detail = {}
        self.DFA ={}
        self.Simple_DFA=[]


        for (node,info) in self.NFA.iteritems():
            for edge in self.NFA_info['edge']:
                if info.has_key(edge):
                    pass
                else:
                    info.setdefault(edge,[])

            if info.has_key('epsilon'):
                pass
            else:
                info.setdefault('epsilon',[])


        for (node,info) in self.NFA.iteritems():
            closurelist = [node]
            newlist = []
            for newnode in info['epsilon']:
                if newnode !=node:
                    newlist.append(newnode)
            self.update_closure(closurelist,newlist)
            closurelist.sort()
            self.ee_closure.setdefault(node,closurelist)

        #print "eeclosrue:"
        #print self.ee_closure
        self.DFA_detail = {}
        self.DFA ={}
        self.Simple_DFA=[]
        self.DFAcounter =0
        self.update_DFA(self.DFA_detail,self.ee_closure[self.NFA_info['start']],self.DFA)

        #print "DFA_detail:"
        #print self.DFA_detail


        #print "DFA"
        #print self.DFA


        self.Simple_DFA.append([])
        for (node,detail) in self.DFA_detail.iteritems():
            self.Simple_DFA[0].append(node)

        count=0
        for (endnode,enddetail) in self.NFA_info['end'].iteritems():
            self.Simple_DFA.append([])
            count = count+1
            for (node,detail) in self.DFA_detail.iteritems():
                for nfanode in detail:                        
                    if endnode==nfanode:
                        self.Simple_DFA[count].append(node)
                        if node in self.Simple_DFA[0]:
                            self.Simple_DFA[0].remove(node)
                        

        #print "Simple_DFA"
        if not self.Simple_DFA[0]:
            self.Simple_DFA.pop(0)
        #print self.Simple_DFA
        dotime =1
        re = 1
        while re==1:
            

            for statelist in self.Simple_DFA:
                re = 0
                for edge in self.NFA_info['edge']:
                    newstatelist=[]
                    origin=-1
                    if self.DFA[statelist[0]].has_key(edge):
                        origin = self.DFA[statelist[0]][edge]

                    
                    for node in statelist:

                        des = -1
                        if self.DFA[node].has_key(edge):
                            des = self.DFA[node][edge]
                        
                        #print 'node',node,'edge',edge,'des',des
                        if des!=origin:
                            newstatelist.append(node);

                    if newstatelist:
                        for node in newstatelist:
                            statelist.remove(node)
                        self.Simple_DFA.append(newstatelist)
                        re = 1
                        break
                if re==1:
                    #print "Simple_DFA_update!"
                    #print self.Simple_DFA
                    break



        #print "Simple_DFA"
        #print self.Simple_DFA

        self.s_DFA ={}
        self.s_DFA_INFO ={'start':-1,'end':{}}

        newstate_num=-1
        for statelist in self.Simple_DFA:
            newstate_num+=1
            for nodelist in statelist:
                for node in self.DFA_detail[nodelist]:
                    #检测节点中有无起始点
                    
                    if node == self.NFA_info['start']:
                        self.s_DFA_INFO['start']=newstate_num;

                    for (endnode,enddetail) in self.NFA_info['end'].iteritems():
                        if node == endnode:
                            self.s_DFA_INFO['end'].setdefault(newstate_num,enddetail)

                    #画边
            self.s_DFA.setdefault(newstate_num,{})
            for nodelist in statelist:
                for edge in self.NFA_info['edge']:
                    if self.DFA[nodelist].has_key(edge):
                        whitchlist = -1
                        for statlist in self.Simple_DFA:
                            whitchlist +=1      #寻找边落到的点在哪个状态
                            for dstnode in statlist:
                                if dstnode == self.DFA[nodelist][edge]:
                                        #if whitchlist!=newstate_num:
                                    self.s_DFA[newstate_num].setdefault(edge,whitchlist)

    # 使用DFA判断输入
    def judgeString(self,target,spmap):

        step = self.s_DFA_INFO['start']
        obj =""
        res = []

        for edge in target:
            
            if self.s_DFA[step].has_key(edge):
                obj += edge
                step = self.s_DFA[step][edge]
            else:
                if self.s_DFA_INFO['end'].has_key(step):
                    if self.s_DFA_INFO['end'][step] == 'NAME' and spmap.has_key(obj):
                        res.append({'category':obj, 'mention':obj})
                    else :
                        res.append({'category':self.s_DFA_INFO['end'][step], 'mention':obj})
                else:
                    print u"未走到终态"
                obj=""
                step = self.s_DFA_INFO['start']
                if self.s_DFA[step].has_key(edge):
                    obj +=edge
                    step = self.s_DFA[step][edge]
                else:
                    print u"刚刚返回初始态后，仍找不到边，字符串有误",obj
        if self.s_DFA_INFO['end'].has_key(step):
              print self.s_DFA_INFO['end'][step]
        else:
              print u"最后一个没有状态"
        return res

    #
    def draw(self):
        g = nx.MultiDiGraph()
        for id,path in self.s_DFA.iteritems():
            for label, to_id in path.iteritems():
                g.add_edge(id,to_id,label=label)
        name = 'dfa'
        nx.write_dot(g, name + '.dot')      
        g = pydot.graph_from_dot_file(name+'.dot')
        g.write_jpg(name+'.jpg')
        print self.s_DFA



#with open('data.txt','r') as f:
#    data = pickle.load(f)
#    dic = data[0]
#    info = data[1]

#print dic


#dfacreator = DFAmanager(dic,info)
##dfacreator.printdetail()
#dfacreator.creatDFA()
#dfacreator.judgeString('abbbbcdd x')
            

    
    





