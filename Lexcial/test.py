#coding=utf8
#import networkx as nx
#import pydot

#g = nx.MultiDiGraph()
#g.add_node(1)

#g.add_node(2)

#g.add_edge(1,2)
#g.add_edge(1,3)
#g.add_node(3)
#name = 'dfa'
#nx.write_dot(g, name + '.dot')      
#g = pydot.graph_from_dot_file(name+'.dot')
#g.write_jpg(name+'.jpg')


#a = set([2,3])
#b = set([2,4])
#a |= b
#print a

class A():
    def __init__(self):
        pass
    def xxx(self):
        print 123
    def x(self, f):
        f()

a = A()

f = a.xxx
a.x(f)