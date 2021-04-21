from common.connections import connectionsSentece
from common.convert import txt2string
from common.parse import textParsed
from common.graph import connections2igraph
from common.graph import delete_separeted_vertices
from igraph import *
import argparse

def generateSentence(listaNomes, arquivoTexto, sentenceNumbers=3):

	listaNomes = txt2string(listaNomes).split('\n')

	text = txt2string(arquivoTexto)
	text = textParsed(text)

	connections = connectionsSentece(text, listaNomes, sentenceNumbers)

	graph = connections2igraph(connections)

	delete_separeted_vertices(graph)

	return graph


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Connections analyzer')
	parser.add_argument('files', metavar='files', type=str, nargs=2, required=True,
                        help='Path to file with a list of words to search and the file with the text')
    parser.add_argument('-d', '--delay', type=float, metavar='delay',
                        default=5.0,
                        help='Time allocated for players to make a move.')

    parser.add_argument('-r', '--redir-stdout', dest='redir_stdout', type=str,
                        default=None, metavar='stdout-file',
                        help='File to redirect players output')

    parser.add_argument('-l', '--log-history', type=str, dest='history',
                        default='history.txt', metavar='log-history',
                        help='File to save game log (history).')

    parser.add_argument('-o', '--output-file', type=str, dest='output',
                        default='results.xml', metavar='output-file',
                        help='File to save game details (includes history)')
	
	
	graph = generateSentence('listaNomes.txt', 'book1.txt')
	
	

	plot(graph)