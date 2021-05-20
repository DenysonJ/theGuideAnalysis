from common.connections import connectionsSentence, connectionsText, joinNodes
from common.convert import txt2string,pdf2string
from common.parse import textParsed
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

def connectionsChapter(listaNomes, arquivoTexto, args):

    listaNomes = txt2string(listaNomes).split('\n')

    connections = {}

    text = pdf2string(arquivoTexto, [page])
    chapters = textParsed(text).split(args.word)

    for chapter in chapters:
        connections = connectionsText(chapter, listaNomes, connections)

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


def parser_connections():
    parser = argparse.ArgumentParser(description='Connections to graph')
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

    group.add_argument('-w', '--word-chapter', type=str, dest='word', 
                        default=None, metavar='word-chapter',
                        help='Word to split the text into chapters.')

    parser.add_argument('-g', '--graph-file', type=str, 
                        default='graph_file.gml', metavar='graph-file',
                        help='File to save the graph generated.')

    parser.add_argument('-j', '--join', type=str, 
                        default=None, metavar='join',
                        help='File with words to join after connection analysis.')

    parser.add_argument('-a', '--attributes', type=str, 
                        default=None, metavar='path-to-attributes',
                        help='Path to file with attributes for all words')

    return parser


if __name__ == '__main__':
    
    args = parser_connections().parse_args()

    if args.sentences:
        graph = generateSentenceConnections(args.words, args.text, args)
        graph.save(args.graph_file)
        sys.exit()

    if args.mode_text:
        graph = generateConnections(args.words, args.text, args)
        graph.save(args.graph_file)
        sys.exit()

    if args.word:
        graph = connectionsChapter(args.words, args.text, args)
        graph.save(args.graph_file)
        sys.exit()

    Ipage, Fpage = args.pages
    graph = connectionsPage(args.words, args.text, range(Ipage, Fpage),args)
    graph.save(args.graph_file)