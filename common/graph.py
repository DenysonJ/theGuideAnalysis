"""
Author: Denyson Grellert
"""

from igraph import *

def connections2igraph(connections):
	g = Graph()

	g.add_vertices(len(connections))
	g.vs["name"] = list(connections.keys())
	g.vs["label"] = g.vs["name"]

	for a in connections:
		for b in connections[a]:
			g.add_edges([(a,b)])
			g[a,b] = connections[a][b]

	return g

def delete_separeted_vertices(graph):

	degrees = graph.degree()

	remove = [i for i in range(len(degrees)) if degrees[i] == 0]

	graph.delete_vertices(remove)