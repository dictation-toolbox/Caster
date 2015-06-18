'''
Created on May 27, 2015

@author: dave
'''
import re

from dragonfly import IntegerRef, Dictation, Text, MappingRule, ActionBase

from caster.lib.dfplus.state.actions import ContextSeeker
from caster.lib.dfplus.state.short import L, S


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
        self.active = False
        # 0 is the first set of children
        self.explode_depth = 1  # the level at which to turn all children into rules
    
    def explode_children(self, depth, max=False):
        results = [self.get_spec_and_text_and_node()]
        depth -= 1
        if depth>=0 or max:
            for child in self.children:
#                 print depth, [x[0] for x in results]
                e = child.explode_children(depth, max)
                for t in e:
                    results.append((results[0][0] + " " + t[0], results[0][1] + t[1], t[2]))
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
            
            action = None
            if node_rule.post!=None:
                action = Text(text)+NodeChange(node_rule, node)+node_rule.post
            else:
                action = Text(text)+NodeChange(node_rule, node)
            mapping[spec] = action

class NodeRule(MappingRule):
    master_node = None
    stat_msg = None
    
    def set_grammar(self, grammar):
        '''for when the grammar is not known in advance'''
        self.grammar = grammar
    
    def __init__(self, node, grammar, stat_msg=None, is_reset=False):
        # for self modification
        self.node = node
        first = False
        if self.master_node == None:
            self.master_node = self.node
            first = True
            self.post = ContextSeeker(None,
                [L(
                S(["cancel"], self.reset_node, None),
                S([self.master_node.text] + [x[0] for x in self.master_node.explode_children(0, True)], lambda: False, None)
                )     ], rspec=self.master_node.text, consume=False)
        if self.stat_msg == None:
            self.stat_msg = stat_msg
        
#         print len(self.node.explode_children(0, True))
        
        mapping = {}
        extras = []
        defaults = {}
        
        # each child node gets turned into a mapping key/value
        for child in self.node.children:
            child.fill_out_rule(mapping, extras, defaults, self)
        
        if len(mapping)==0:
            if self.stat_msg!=None and not first:
                self.stat_msg.text("Node Reset")# status window messaging
            self.reset_node()
            for child in self.node.children:
                child.fill_out_rule(mapping, extras, defaults, self)
        else:
            if self.stat_msg!=None and not first and not is_reset:# status window messaging
                self.stat_msg.hint("\n".join([x.get_spec_and_text_and_node()[0] for x in self.node.children]))
        
#         print [x for x in mapping]
        
        MappingRule.__init__(self, "node_" + str(self.master_node.text), mapping, extras, defaults)
        self.grammar = grammar
        
    
    def change_node(self, node, reset=False):
        self.grammar.unload()
#         print "grammar: ", self.grammar
        NodeRule.__init__(self, node, self.grammar, None, reset)
        self.grammar.load()
    
    def reset_node(self):
        self.change_node(self.master_node, True)
    
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

