'''
Created on May 27, 2015

@author: dave
'''
import re

from dragonfly import IntegerRef, Dictation, Text, MappingRule


# for creating extras and defaults
NUMBER_PATTERN_PUNC = re.compile('(%\([0-9A-Za-z_]+\)d)')
STRING_PATTERN_PUNC = re.compile('(%\([0-9A-Za-z_]+\)s)')
NUMBER_PATTERN = re.compile('%\(([0-9A-Za-z_]+)\)d')
STRING_PATTERN = re.compile('%\(([0-9A-Za-z_]+)\)s')

class HintNode:
    def __init__(self, text, children=[], spec=None):
        self.text = text
        self.children = children
        self.spec = spec
        self.parent = None
        for child in self.children:
            child.set_parent(self)
    def set_parent(self, parent):
        self.parent = parent
    def fill_out_rule(self, mapping, extras, defaults):
        spec = self.text
        if self.spec!=None and len(self.spec) > 0:
            spec = ""
            not_first = False
            for pronunciation in self.spec:
                if not_first:
                    spec += " | "
                spec += pronunciation
                not_first = True
        
        
       
        # generate extras, defaults, and spec based on node text
        global NUMBER_PATTERN_PUNC, STRING_PATTERN_PUNC, NUMBER_PATTERN, STRING_PATTERN
        numbers = NUMBER_PATTERN_PUNC.findall(self.text)
        strings = STRING_PATTERN_PUNC.findall(self.text)
        for n in numbers:
            word = NUMBER_PATTERN.findall(n)[0]
            spec = spec.replace(n, "<" + word + ">")
            extras.append(IntegerRef(word, 0, 10000))
            defaults[word] = 1
        for s in strings:
            word = STRING_PATTERN.findall(s)[0]
            spec = spec.replace(s, "<" + word + ">")
            extras.append(Dictation(word))
            defaults[word] = ""
        
        
        # for node compression (speaking multiple nodes in one utterance)
        spec += " [<next_nodes>]"
        mapping[spec] = Text(self.text)

class NodeRule(MappingRule):
    master_node = None
    
    def set_grammar(self, grammar):
        '''for when the grammar is not known in advance'''
        self.grammar = grammar
    
    def __init__(self, node, grammar):
        self.grammar = grammar # for self modification
        self.node = node
        if self.master_node==None:
            self.master_node=self.node
        
        if grammar:
            grammar.unload()
        
        mapping = {}
        extras = []
        defaults = {}
        
        # each child node gets turned into a mapping key/value
        for child in node.children:
            child.fill_out_rule(mapping, extras, defaults)
        extras.append(Dictation("next_nodes"))
        defaults["next_nodes"] = ""
        
        MappingRule.__init__(self, "node_" + str(self.master_node.text), mapping, extras, defaults)
        
        
    
    def change_node(self, node):
        self.__init__(node, self.grammar)
    
    def reset_node(self):
        self.__init__(self.master_node, self.grammar)
    
    def _process_recognition(self, node, extras):
        
        node._action.execute(node._data)
#         MappingRule._process_recognition(self, value, extras)
        new_node = None
        results = extras["_node"].results
        print results
        # background 100background bar
#         Text(self.node.text).execute(node._data)
        if extras["next_nodes"]!="":
            '''attempt to parse out further nodes-- print them, then set new_node to last'''
        
#         self.grammar.unload()
#         self.change_node(new_node)
#         self.grammar.load()
    

def node_into_rule(node):
    ''''''
