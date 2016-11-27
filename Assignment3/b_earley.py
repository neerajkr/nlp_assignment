
class State(object):			# State in earley algo
    def __init__(self, name, production, dot_index, start_column):  # constructor for initialisation
        self.name = name	  #Rule name			
        self.production = production   # production rule    
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index  # dot position in the sate
        self.rules = [t for t in production if isinstance(t, Rule)]
    def __repr__(self):			#representation of a state
        terms = [str(p) for p in self.production]
        terms.insert(self.dot_index, u"$")
        return "%-5s -> %-16s [%s-%s]" % (self.name, " ".join(terms), self.start_column, self.end_column)
    def __eq__(self, other):      # comapring two states, if they are equal
        return (self.name, self.production, self.dot_index, self.start_column) == \
            (other.name, other.production, other.dot_index, other.start_column)
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        return hash((self.name, self.production))
    def completed(self):   #checking whether a state is compled if its dot index is at last position
        return self.dot_index >= len(self.production)
    def next_term(self):		#predict next state
        if self.completed():    #if a state is complete then return none
            return None
        return self.production[self.dot_index]





class Column(object):			# for each word in a string, there will be a column and each col will have states, as taught in class
    def __init__(self, index, token):   # constructor
        self.index = index    # column index (index starts from 0 to number of words)
        self.token = token  #token or words from a test sentence
        self.states = []     #initialising states to empty
        self._unique = set() # a set to ensure unique state in each column, no need of same element more than once
    def __str__(self):
        return str(self.index)  
    def __len__(self):
        return len(self.states)  # returning number of states in a particular column
    def __iter__(self):
        return iter(self.states)
    def __getitem__(self, index):
        return self.states[index]  #retun states in a partiular column defined by index
    def enumfrom(self, index):
        for i in range(index, len(self.states)):
            yield i, self.states[i]
    def add(self, state):    # adding a states to column
        if state not in self._unique:  #checking to ensure that , state does not already exists
            self._unique.add(state)
            state.end_column = self
            self.states.append(state)
            return True
        return False
    def print_(self, completedOnly = False):  # printing the states of a particular colmn
        print "[%s] %r" % (self.index, self.token)
        print "=" * 35
        for s in self.states:
            if completedOnly and not s.completed():
                continue
            print repr(s)
        print




class Production(object):
    def __init__(self, *terms):				#constructor for intialising
        self.terms = terms  # in A->"book", terms is book
    def __len__(self):		    # can be used to return the number of terminals/non-terminals on right side for a unique left side non-terminal
        return len(self.terms)
    def __getitem__(self, index):  # given a index, return terminal/non-temrinal
        return self.terms[index]
    def __iter__(self):     
        return iter(self.terms)
    def __repr__(self):    # can be used to visualise the production rule
        return " ".join(str(t) for t in self.terms)
    def __eq__(self, other):  # checking whether the rule already exist
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms #reutn 1 , if already exist
    def __ne__(self, other):
        return not (self == other)  
    def __hash__(self):
        return hash(self.terms)



class Rule(object):     # Grammar rules
    def __init__(self, name, *productions):  #constructor to add grammar rules
        self.name = name
        self.productions = list(productions)
    def __str__(self):	
        return self.name
    def __repr__(self):			# Represent the grammar in usual symbol
        return "%s -> %s" % (self.name, " | ".join(repr(p) for p in self.productions))
    def add(self, *productions):			#adding rules to exisitng grammar
        self.productions.extend(productions)


class Node(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def print_(self, level = 0):
        print "  " * level + str(self.value)
        for child in self.children:
            child.print_(level + 1)

def predict(col, rule):			# given column and rule, predict and add a new state
    for prod in rule.productions:
        col.add(State(rule.name, prod, 0, col)) 

def scan(col, state, token):   # scan rule and incrementing the dot index position
    if token != col.token:
        return
    col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))


# for every state in a column, find states in all other column and add after checking the constraint
# to the same column

def complete(col, state):  
    if not state.completed():
        return
    for st in state.start_column:
        term = st.next_term()
        if not isinstance(term, Rule):
            continue
        if term.name == state.name:
            col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))

S_0_RULE = u"S_0"    # starts position for parse tree

def Parse(rule, text):
    table = [Column(i, tok) for i, tok in enumerate([None] + text.lower().split())]  # table of columns and states
    # in the table, number of columns is 1+len(words), as explained in class
    table[0].add(State(S_0_RULE, Production(rule), 0, table[0]))   # initialising first column of table

    for i, col in enumerate(table):   # filling all the table rules
        for state in col:    # for each state in a particular column, checking the dot_index either complete,predict,or scan
            if state.completed():
                complete(col, state)
            else:
                term = state.next_term()
                if isinstance(term, Rule):    # If rule exists then predict it
                    predict(col, term)
                elif i + 1 < len(table):        # if rule doesn't exist and there is a next column, add it
                    scan(table[i+1], state, term)

    # find S_0 rule in last table column (otherwise fail)
    for st in table[-1]:      # in last column, if state is completed and S_0(start) exists,means grammar is able to Parse
        if st.name == S_0_RULE and st.completed():
            return(st)
    else:
        raise ValueError("parsing failed")

def BuildTrees(state):
    return BuildTreesHelper([], state, len(state.rules) - 1, state.end_column)


# Build the tree and print it 

# S_0   -> S $              [0-6]
#   S     -> X1 VP $          [0-6]
#     X1    -> AUX NP $         [0-3]
#       AUX   -> does $           [0-1]
#       NP    -> DET NOMINAL $    [1-3]
#         DET   -> the $            [1-2]
#         NOMINAL -> flight $         [2-3]
#     VP    -> VERB NP $        [3-6]
#       VERB  -> include $        [3-4]
#       NP    -> DET NOMINAL $    [4-6]
#         DET   -> a $              [4-5]
#         NOMINAL -> meal $           [5-6]

# for example in the above, the S_0 is start position and ans space from begining 
# represent the depth of that level in tree, index in brackets represent the state, which was used for
# either scan, predict or complete, depending upon constraints


def BuildTreesHelper(children, state, rule_index, end_column):
    if rule_index < 0:
        return [Node(state, children)]
    elif rule_index == 0:
        start_column = state.start_column
    else:
        start_column = None
    
    rule = state.rules[rule_index]
    outputs = []
    for st in end_column:
        if st is state:
            break
        if st is state or not st.completed() or st.name != rule.name:
            continue
        if start_column is not None and st.start_column != start_column:
            continue
        for sub_tree in BuildTrees(st):
            for node in BuildTreesHelper([sub_tree] + children, state, rule_index - 1, st.start_column):
                outputs.append(node)
    return outputs


########################## Grammar Rules ###################################

AUX=Rule("AUX",Production("does"))   # this defines AUX->"does"

PREPOSITION=Rule("PREPOSITION",Production("from"),Production("to"),Production("on"),
    Production("near"),Production("through")) #this defines PREPOSITION->"from"|"to"|"on"|"near"|"through"

DET=Rule("DET",Production("that"),Production("this"),Production("a"),Production("the")) #similar as above two

NOUN=Rule("NOUN",Production("book"),Production("flight"),Production("meal"),Production("money"))

VERB=Rule("VERB",Production("book"),Production("include"),Production("prefer"))

PRONOUN=Rule("PRONOUN",Production("I"),Production("she"),Production("me"))

PROPER_NOUN=Rule("PROPER_NOUN",Production("TWA"),Production("Houston"))


NP=Rule("NP",Production("I"),Production("she"),Production("me"),Production("TWA"),
    Production("Houston"))

X1=Rule("X1",Production(AUX, NP))
X2=Rule("X2",Production(VERB,NP))

PP=Rule("PP",Production(PREPOSITION),Production(NP))


NOMINAL=Rule("NOMINAL",Production("book"),Production("flight"),Production("meal"),Production("money"))

NP.add(Production(DET,NOMINAL))  # .add() function simply adds a new rule to existing production
NOMINAL.add(Production(NOMINAL,NOUN),Production(NOMINAL,PP))

VP=Rule("VP",Production("book"),Production("include"),Production("prefer"),Production(VERB,NP),
    Production(X2,PP),Production(VERB,PP))
VP.add(Production(VP,PP))


S=Rule("S",Production(NP,VP),Production(X1,VP),Production("book"),Production("include"),
    Production("prefer"),Production(VERB, NP),Production(X2,PP),Production(VERB,PP),
    Production(VP,PP))


################# Parse Output #######################

sentence="does the flight include a meal" # sentence to parse
# text=sentence
# for i, tok in enumerate([None] + text.lower().split()):
#     print i
#     print tok
for tree in BuildTrees(Parse(S, sentence)): #call BuildTrees function to parse the tree
    print "-"*50
    tree.print_()














