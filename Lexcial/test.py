#coding=utf8
import networkx as nx
import pydot

g = nx.MultiDiGraph()
g.add_node(1)

g.add_node(2)

g.add_edge(1,2)
g.add_edge(1,3)
g.add_node(3)
name = 'dfa'
nx.write_dot(g, name + '.dot')      
g = pydot.graph_from_dot_file(name+'.dot')
g.write_jpg(name+'.jpg')