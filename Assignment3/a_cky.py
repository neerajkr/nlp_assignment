
from collections import defaultdict         #importing library
from itertools import product

def CYKalgo(words, rules):          # Main CYK algo
    table = defaultdict(lambda : defaultdict(list))  #
    # print table
    BackPtr = defaultdict(lambda : defaultdict(lambda : defaultdict(list)))  #back-pointer 
    # print BackPtr
    for j in xrange(len(words)):
        for A in rules[tuple([words[j]])]: #all derivations, A that  A -> words[j]
            # print A
            # print j
            table[j-1][j].append(A)  # Initialising the table for each single word
            BackPtr[j-1][j][A].append(words[j])  #Intialising the Back ptr for generating each word

        for i in xrange(j-2, -2, -1):   #range od the span
            for k in xrange(i+1, j):        #partition of the span
                for B, C in product(table[i][k], table[k][j]): #for each partition
                    for A in rules[(B, C)]: #if the rule exist for each part then update table and backpointer
                        table[i][j].append(A)
                        BackPtr[i][j][A].append(((i,k,B), (k,j, C)))


# Implementation to get element from Backptr and make a tree,
 # where brackets indicate the association in trees

    def recons(BackPtr, i, j, sym):     #Using the backpointer of defaultdict data str to reconstruct the tree
        
        trees = []
        if len(BackPtr[i][j][sym]) == 1 and isinstance(BackPtr[i][j][sym][0], str): # checking for terminals
            return [(sym, BackPtr[i][j][sym][0])]
        else:
            for p1, p2 in BackPtr[i][j][sym]: # if backkptr is does not contents only terminals then iterate through indices
                i,k,B = p1
                k,j,C = p2
                for left_tree, right_tree in product(recons(BackPtr, i, k, B),
                                                     recons(BackPtr, k, j, C)):
                    trees.append((sym, left_tree, right_tree))  # append left and right part of subtree
            return trees

    return recons(BackPtr, -1, len(words)-1, "S")       #return the tree


###################### Grammar Rules ###########################################


GrammarRules = [

    ("S", ("NP", "VP")),
    ("S", ("X1", "VP")),
    ("S", ("book",)),
    ("S", ("include",)),
    ("S", ("prefer",)),
    ("S", ("VERB", "NP")),
    ("S", ("X2", "PP")),
    ("S", ("VERB", "PP")),
    ("S", ("VP", "PP")),

    ("X1", ("AUX", "NP")),

    ("NP", ("I",)),
    ("NP", ("she",)),
    ("NP", ("me",)),
    ("NP", ("TWA",)),
    ("NP", ("Houston",)),
    ("NP", ("DET", "NOMINAL")),

    ("NOMINAL", ("book",)),
    ("NOMINAL", ("flight",)),
    ("NOMINAL", ("meal",)),
    ("NOMINAL", ("money",)),
    ("NOMINAL", ("NOMINAL", "NOUN")),
    ("NOMINAL", ("NOMINAL", "PP")),

    ("VP", ("book",)),
    ("VP", ("include",)),
    ("VP", ("prefer",)),
    ("VP", ("VERB", "NP")),
    ("VP", ("X2", "PP")),
    ("VP", ("VERB", "PP")),
    ("VP", ("VP", "PP")),

    ("X2", ("VERB", "NP")),

    ("PP", ("PREPOSITION", "NP")),

    ("DET", ("that" )),
    ("DET", ("this", )),
    ("DET", ("a", )),
    ("DET", ("the", )),

    ("NOUN", ("book", )),
    ("NOUN", ("flight", )),
    ("NOUN", ("meal", )),
    ("NOUN", ("money", )),

    ("VERB", ("book", )),
    ("VERB", ("include", )),
    ("VERB", ("prefer", )),

    ("PRONOUN", ("I", )),
    ("PRONOUN", ("she", )),
    ("PRONOUN", ("me", )),

    ("PROPER-NOUN", ("TWA", )),
    ("PROPER-NOUN", ("Houston", )),

    ("AUX", ("does", )),

    ("PREPOSITION", ("from", )),
    ("PREPOSITION", ("to", )),
    ("PREPOSITION", ("on", )),
    ("PREPOSITION", ("near", )),
    ("PREPOSITION", ("through", )),
]


def IndexRules(rules):
    indexing = defaultdict(list)
    for A,B in rules:
        indexing[B].append(A)
    # print indexing
    return indexing

sentence="a flight from Houston to TWA"

# print sentence.split()
for tree in CYKalgo(sentence.split(), IndexRules(GrammarRules)):
    print tree