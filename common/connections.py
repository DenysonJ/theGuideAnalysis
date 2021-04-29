"""
Author: Denyson Grellert
"""

from re import search as reSearch
import spacy

#Functions to create connections between nodes given a list of words (or names)

"""
Set all connections between nodes. The function will sum 1 to the current value
of connection of the nodes to keep track of how many times they are connected

    Args:
        namesToConnect 	-> list of all words that need to be connected with each other
        connections 	-> current connections

    It's expected that connections are already initialized with all names with
    a dictionary as value, where will be set all connections 

    Return:
        None

    All connections will be set in the connections argument
"""
def setConnections(namesToConnect, connections):
    notConnected = namesToConnect.copy()

    for name in namesToConnect:
        notConnected.remove(name)
        for key in connections:
            if key in notConnected:
                connections[key][name] = 1 + connections[key].get(name, 0)


"""
Set all connections between nodes in a sentence. 

    Args:
        text  (string)			-> text to separate in sentences and search the connections 
                                    between names/words
        names (list - string)	-> list of all names/words to search for connections
        connections (dictionary)-> current connections
        sentenceNumbers (int)   -> number of sentences to make connections

    Return:
        connections (dictionary) -> The keys are the names given and the values
                                    are dictionaries with the connections among the names
"""
def connectionsSentece(text, names, connections={}, sentenceNumbers=4):

    if not connections:
        for name in names:
            connections[name] = {}

    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)

    number = 0
    sentences = []
    for sent in doc.sents:
        sentences.append(sent.text)
        string = " ".join(sentences)
        connect = [name for name in names if reSearch(r'\b'+name.lower()+r'\b',string.lower())]

        setConnections(connect, connections)

        if number < sentenceNumbers:
            number += 1
            continue

        del sentences[0]

    return connections


"""
Set all connections between nodes in a text. 

    Args:
        text  (string)			-> text to search the connections between names/words
        names (list - string)	-> list of all names/words to search for connections
        connections (dictionary)-> current connections

    Return:
        connections (dictionary) -> The keys are the names given and the values
                                    are dictionaries with the connections among the names
"""
def connectionsText(text, names, connections={}):

    if not connections:
        for name in names:
            connections[name] = {}

    connect = [name for name in names if reSearch(r'\b'+name.lower()+r'\b',text.lower())]

    setConnections(connect, connections)

    return connections


"""
Join nodes in a dictionary with connections
This can be usefull when a person or a thing is referenced in the text
by her first or last name. Put both in the name list to be searched, 
and then join the nodes later.

    Args:
        connections (dictionary) -> current connections

    Return:
        None

"""
def joinNodeConnections(listNames, connections):
    first = [i[0] for i in listNames]
    second = [i[1] for i in listNames]

    for pair in listNames:
        for name in connections[pair[0]]:
            if name in second:
                connections[pair[0]][first[second.index(name)]] = connections[pair[0]].get(name, 0) + connections[pair[1]].get(name, 0)
                del connections[pair[1]][name]
                continue

            connections[pair[0]][name] = connections[pair[0]].get(name, 0) + connections[pair[1]].get(name, 0)
            del connections[pair[1]][name]

        for name in connections[pair[1]]:
            if name in second:
                connections[pair[0]][first[second.index(name)]] = connections[pair[0]].get(name, 0) + connections[pair[1]].get(name, 0)
                continue

            connections[pair[0]][name] = connections[pair[0]].get(name, 0) + connections[pair[1]].get(name, 0)

        del connections[pair[1]]