'''
Created on May 27, 2015

@author: dave
'''
import re

from dragonfly import IntegerRef, Dictation, Text, MappingRule, ActionBase

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
        # 0 is the first set of children
        self.explode_depth = 1 # the level at which to turn all children into rules
        
    def set_parent(self, parent):
        self.parent = parent
    def get_node_from_speech_results(self, results):
        '''results is a tuple of tuples, (word, code)'''
        '''only returns null if there are no children'''
        nodes = self.children
        best_node = (None, 0)
        for node in nodes:
            score=0
            points=len(results)
            for result in results:
                if result[1]==1:# code 1 is spoken literal, 5=number parameter, 1mil=string parameter
                    if node.text==result[0]:
                        return node
                    else:
                        text_to_check=node.text
                        if node.spec!=None:
                            for pronunciation in node.spec:
                                text_to_check += " "+pronunciation
                        if result[0] in text_to_check:
                            score += points 
                        points -= 1 # penalize words that are later on in the results, in case words appear more than once
                        
            print node.text, " :: ", score                
            if score>best_node[1]:
                best_node=(node, score)
        return best_node[0]
    
    def explode_children(self, depth):
        results = [self.get_spec_and_text_and_node()]
        depth -= 1
        if depth>=0:
            for child in self.children:
                e = child.explode_children(depth)
                for t in e:
#                     results.append(results[0] + " " + s)
                    results.append((results[0][0] + " " + t[0], results[0][1] + " " + t[1], t[2]))
        return results
    
    def get_spec_and_text_and_node(self):
        spec = self.text # defaults spec to text
        text = self.text 
        if self.spec!=None and len(self.spec) > 0:
            spec = ""
            not_first = False
            for pronunciation in self.spec:
                if not_first:
                    spec += " | "
                spec += pronunciation
                not_first = True
            spec += ""
        return (spec, text, self)
            
    def fill_out_rule(self, mapping, extras, defaults, node_rule):
#         utilities.remote_debug("fill_out_rule")
        specs = self.explode_children(self.explode_depth)
        if len(specs)>1:
            specs.append(self.get_spec_and_text_and_node())
        
        
        
        # generate extras, defaults, and spec based on node text
        global NUMBER_PATTERN_PUNC, STRING_PATTERN_PUNC, NUMBER_PATTERN, STRING_PATTERN
        for spec, text, node in specs:
            numbers = NUMBER_PATTERN_PUNC.findall(text)
            strings = STRING_PATTERN_PUNC.findall(text)
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
        
            mapping[spec] = Text(text)+NodeChange(node_rule, node)

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
        for child in self.node.children:
            child.fill_out_rule(mapping, extras, defaults, self)
        print [x for x in mapping]
        
        MappingRule.__init__(self, "node_" + str(self.master_node.text), mapping, extras, defaults)
        self.grammar = grammar
        
    
    def change_node(self, node):
        self.grammar.unload()
        NodeRule.__init__(self, node, self.grammar)
        self.grammar.load()
    
    def reset_node(self):
        self.change_node(self.master_node)
    
    def _process_recognition(self, node, extras):
        '''
        There are two kinds of nodes being referred to in here: Dragonfly _processor_recognition nodes, 
        and Caster hintnode.HintNode(s). "node" is the former, "self.node" is the latter.
        '''
        node=node[self.master_node.text]
        node._action.execute(node._data)
        
    
class NodeAction(ActionBase):
    def __init__(self, node_rule):
        ActionBase.__init__(self)
        self.node_rule = node_rule
    def _execute(self, data):
        self.node_rule._process_recognition(data, None)

class NodeChange(ActionBase):
    def __init__(self, node_rule, node):
        ActionBase.__init__(self)
        self.node_rule = node_rule
        self.node = node
    def _execute(self, data):
        self.node_rule.change_node(self.node)

