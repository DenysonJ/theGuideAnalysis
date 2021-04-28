"""
Author: Denyson Grellert
"""

from igraph import *

"""
Makes a graph from a dictionary with all connections between the nodes
    
    Args:
        connections (dictionary) -> A dictionary with the nodes and the connections
                                    between them

    Return:
        g (igraph) -> graph with all nodes in connections and edges where exist a connection
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
        graph (igraph)	-> A graph

    Return:
        graph (igraph)  -> graph without separeted vertices
"""
def delete_separeted_vertices(graph):

    degrees = graph.degree()

    remove = [i for i in range(len(degrees)) if degrees[i] == 0]

    graph.delete_vertices(remove)


"""
Receive a graph and save the graph properties

    Args:
        graph (igraph)  -> The graph to be analyzed
        output_filename (string) -> Name to output

    Return:
        None
"""
def graph_properties(graph, output_filename="results.txt"):
    b = graph.betweenness()
    c = graph.closeness()
    p = graph.pagerank(directed = False)

    string = ""

    string += "Shortest Average Path Length: " + str(graph.average_path_length())
    string += "\nClustering coefficient: " + str(graph.transitivity_undirected(mode="zero"))
    string += "\nDiameter: " + str(graph.diameter())
    string += "\nDensity: " + str(graph.density())
    string += "\n"
    # string += "-"*55
    # # string += "\nDegree distribution:\n"
    # # string += ' '.join(map(str, graph.degree_distribution()))
    # string += "\n"
    string += "-"*55
    string += "\nAverage degree: " + str(sum(graph.vs.degree())/graph.vcount())
    string += "\nVertices with the greatest:"
    string += "\nDegree: " + str(max(graph.vs.degree()))
    string += "\nBetweenness: %d Nodo: %d, %s" % (max(b), b.index(max(b)), graph.vs["name"][b.index(max(b))])
    string += "\nCloseness: %f Nodo: %d, %s" % (max(c), c.index(max(c)), graph.vs["name"][c.index(max(c))])
    string += "\nEigenvector centrality: %s" % (graph.evcent())
    string += "\n"
    string += "-"*55
    string += "\nPageRank max: " + str(max(p))
    string += "\nPageRank:\n"
    string += ' '.join(map(str, p))

    with open(output_filename, 'w') as f:
        f.write(string)