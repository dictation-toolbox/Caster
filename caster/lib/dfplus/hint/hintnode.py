'''
Created on May 27, 2015

@author: dave
'''
import re

from dragonfly import IntegerRef, Dictation, Text, MappingRule

from caster.lib import utilities


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
    def get_child_node_from_speech_results(self, results):
        '''results is a tuple of tuples, (word, code)'''
        '''only returns null if there are no children'''
        best_child = (None, 0)
        for child in self.children:
            score=0
            for result in results:
                if result[1]==4:# code 4 is spoken literal
                    if child.text==result[0]:
                        return child
                    else:
                        text_to_check=child.text
                        if self.spec!=None:
                            for pronunciation in self.spec:
                                text_to_check += " "+pronunciation
                        if result[0] in text_to_check:
                            score += 1
            if score>best_child[1]:
                best_child=(child, score)
        return best_child[0]
                    
            
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
#             spec = spec.replace(n, "<" + word + ">")
            extras.append(IntegerRef(word, 0, 10000))
            defaults[word] = 1
        for s in strings:
            word = STRING_PATTERN.findall(s)[0]
#             spec = spec.replace(s, "<" + word + ">")
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
        # for self modification
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
        self.grammar = grammar
        
    
    def change_node(self, node):
        NodeRule.__init__(self, node, self.grammar)
    
    def reset_node(self):
        NodeRule.__init__(self, self.master_node, self.grammar)
    
    def _process_recognition(self, node, extras):
        utilities.remote_debug("test action")
        node._action.execute(node._data)

        new_node = self.node.get_child_node_from_speech_results(extras["_node"].results)
        
        
        
        if extras["next_nodes"]!="":
            '''attempt to parse out further nodes-- print them, then set new_node to last'''
        
        
        
        self.grammar.unload()
        self.change_node(new_node)
        self.grammar.load()
    

def node_into_rule(node):
    ''''''
