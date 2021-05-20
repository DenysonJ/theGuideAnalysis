from common.graph import *
from igraph import *

def analysis(graph, args):
    colors = None
    if args.color:
        colors = colorsList(len(set(graph.vs[args.color])))

    plot(graph, target=args.graph_file, **visualStyle(graph, color=colors))
    graph_properties(graph, args.output)
    graph_communities(graph, args)


def parser_graph_analysis():
    parser = argparse.ArgumentParser(description='Connections to graph')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    parser.add_argument('graph', metavar='path-to-graph', type=str,
                        help='Path to file with the graph to be analyzed')

    parser.add_argument('-c', '--color-attribute', type=str, dest='color', 
                        default=None, metavar='attribute-name',
                        help='An attribute name to color all nodes equal if they have the same attribute')

    parser.add_argument('-o', '--output-file', type=str, dest='output',
                        default='results', metavar='output-file',
                        help='File to save analysis output')

    parser.add_argument('-g', '--graph-file', type=str, 
                        default='graph_file.gml', metavar='graph-file',
                        help='File to save the graph generated.')


if __name__ == '__main__':
    