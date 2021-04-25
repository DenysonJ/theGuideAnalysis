"""
Author: Denyson Grellert
"""

from igraph import *

"""
Makes a graph from a dictionary with all connections between the nodes
    
    Args:
        connections 	-> A dictionary with the nodes and the connections
                          between them

    Return:
        g -> graph with all nodes in connections and edges where exist a connection
"""
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


"""
Receive a graph and return a graph without separeted vertices

    Args:
        graph 	-> A graph

    Return:
        graph -> graph without separeted vertices
"""
def delete_separeted_vertices(graph):

    degrees = graph.degree()

    remove = [i for i in range(len(degrees)) if degrees[i] == 0]

    graph.delete_vertices(remove)