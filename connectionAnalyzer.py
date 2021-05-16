from common.connections import connectionsSentence, connectionsText, joinNodes
from common.convert import txt2string,pdf2string
from common.parse import textParsed
from common.graph import *
from igraph import *
import argparse
import sys

def generateSentenceConnections(listaNomes, arquivoTexto, args):

    listaNomes = txt2string(listaNomes).split('\n')

    text = txt2string(arquivoTexto)
    text = textParsed(text)

    connections = connectionsSentence(text, listaNomes, sentenceNumbers=args.sentences)

    if args.join:
        pairList = attributesFile(args.join)
        joinNodes(pairList, connections)

    graph = connections2igraph(connections)

    delete_separeted_vertices(graph)

    if args.attributes:
        attrList = attributesFile(args.attributes)
        graph_attributes(graph, attrList)

    return graph

def generateConnections(listaNomes, arquivoTexto, args):

    listaNomes = txt2string(listaNomes).split('\n')

    text = txt2string(arquivoTexto)
    text = textParsed(text)

    connections = connectionsText(text, listaNomes)

    if args.join:
        pairList = attributesFile(args.join)
        joinNodes(pairList, connections)

    graph = connections2igraph(connections)

    delete_separeted_vertices(graph)

    if args.attributes:
        attrList = attributesFile(args.attributes)
        graph_attributes(graph, attrList)

    return graph

def connectionsPage(listaNomes, arquivoTexto, pages, args):

    listaNomes = txt2string(listaNomes).split('\n')

    connections = {}

    for page in pages:
        text = pdf2string(arquivoTexto, [page])
        text = textParsed(text)

        connections = connectionsText(text, listaNomes, connections)

    if args.join:
        pairList = attributesFile(args.join)
        joinNodes(pairList, connections)

    graph = connections2igraph(connections)

    delete_separeted_vertices(graph)

    if args.attributes:
        attrList = attributesFile(args.attributes)
        graph_attributes(graph, attrList)

    return graph

def attributesFile(file):

    splited = txt2string(file).split('\n')

    pairList = []
    for pair in splited:
        pairList.append(pair.split(','))

    return pairList

def visualStyle(graph, color=None, vertex_size=15, window_size=(600, 600), margin=20):

    visual_style = {}
    visual_style["vertex_size"] = vertex_size
    visual_style["edge_width"] = graph.es["weight"]
    visual_style["bbox"] = window_size
    visual_style["margin"] = margin

    if color:
        visual_style["vertex_color"] = color

    return visual_style


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Connections analyzer')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')

    parser.add_argument('words', metavar='path-to-words', type=str,
                        help='Path to file with a list of words to search in the text')
    parser.add_argument('text', metavar='path-to-text', type=str,
                        help='Path to file with the text to be searched')

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-s', '--sentences', type=int,
                        default=None, metavar='number-of-sentences',
                        help='This option will enable connections per sentence, using spacy. Text file must be in txt format.')

    group.add_argument('-t', '--mode-text', action='store_true',
                        help='This option will enable connections in the entire text. Text file must be in txt format.')

    group.add_argument('-p', '--pages', type=int, nargs=2,
                        default=None, metavar='pages',
                        help='This option will enable connections per page. Must be passed the initial and final \
                        page. Text file must be in pdf format.')

    parser.add_argument('-a', '--attributes', type=str, 
                        default=None, metavar='path-to-attributes',
                        help='Path to file with attributes for all words')

    parser.add_argument('-o', '--output-file', type=str, dest='output',
                        default='results', metavar='output-file',
                        help='File to save analysis output')

    parser.add_argument('-g', '--graph-file', type=str, 
                        default='graph_file.gml', metavar='graph-file',
                        help='File to save the graph generated.')

    parser.add_argument('-e', '--extension', type=str, choices=['pdf', 'png', 'svg'], 
                        default='png', metavar='graph-file',
                        help='File to save the graph generated.')

    parser.add_argument('-j', '--join', type=str, 
                        default=None, metavar='join',
                        help='File with words to join after connection analysis.')


    args = parser.parse_args()

    if args.sentences:
        graph = generateSentenceConnections(args.words, args.text, args)
        plot(graph, target=args.graph_file+'Sentence.'+args.extension)
        graph_properties(graph, args.output+"Sentence.txt")
        graph.save(args.graph_file)
        sys.exit()

    if args.mode_text:
        print(args.mode_text)
        sys.exit()
        graph = generateConnections(args.words, args.text, args)
        plot(graph, target=args.graph_file+'.'+args.extension)
        graph_properties(graph, args.output+".txt")
        graph.save(args.graph_file)
        sys.exit()

    Ipage, Fpage = args.pages
    graph = connectionsPage(args.words, args.text, range(Ipage, Fpage),args)
    plot(graph, target=args.graph_file+'.'+args.extension)
    graph_properties(graph, args.output+".txt")
    graph.save(args.graph_file)