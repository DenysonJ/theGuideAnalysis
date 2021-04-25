from common.connections import connectionsSentece, connectionsText
from common.convert import txt2string
from common.parse import textParsed
from common.graph import connections2igraph, delete_separeted_vertices
from igraph import *
import argparse

def generateSentenceConnections(listaNomes, arquivoTexto, sentenceNumbers=3):

    listaNomes = txt2string(listaNomes).split('\n')

    text = txt2string(arquivoTexto)
    text = textParsed(text)

    connections = connectionsSentece(text, listaNomes, sentenceNumbers)

    graph = connections2igraph(connections)

    delete_separeted_vertices(graph)

    return graph

def generateConnections(listaNomes, arquivoTexto):

    listaNomes = txt2string(listaNomes).split('\n')

    text = txt2string(arquivoTexto)
    text = textParsed(text)

    connections = connectionsText(text, listaNomes, sentenceNumbers)

    graph = connections2igraph(connections)

    delete_separeted_vertices(graph)

    return graph


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Connections analyzer')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    parser.add_argument('words', metavar='path-to-words', type=str,
                        help='Path to file with a list of words to search in the text')
    parser.add_argument('text', metavar='path-to-text', type=str,
                        help='Path to file with the text to be searched')

    parser.add_argument('-s', '--sentences', type=int, 
                        default=None, metavar='number-of-sentences',
                        help='')

    parser.add_argument('-n', '--no-text', action='store_false', default=None, 
                        help='')

    parser.add_argument('-a', '--attributes', type=str, 
                        default=None, metavar='path-to-attributes',
                        help='Path to file with attributes for all words')

    parser.add_argument('-o', '--output-file', type=str, dest='output',
                        default='results.txt', metavar='output-file',
                        help='File to save analysis output, without extension')

    parser.add_argument('-g', '--graph-file', type=str, 
                        default='graph_file', metavar='graph-file',
                        help='File to save the graph generated.')

    parser.add_argument('-e', '--extension', type=str, choices=['pdf', 'png', 'svg'], 
                        default='png', metavar='graph-file',
                        help='File to save the graph generated.')



    args = parser.parse_args()


    if args.sentences:
        graph = generateSentenceConnections(args.words, args.text, args.sentences)
        plot(graph, target=args.graph_file+'.'+args.extension)


    if args.no_text:
        graph = generateConnections(args.words, args.text)
        plot(graph, target=args.graph_file+'.'+args.extension)