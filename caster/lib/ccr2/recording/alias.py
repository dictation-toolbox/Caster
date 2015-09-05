'''
Created on Sep 3, 2015

@author: synkarius
'''
import re

from caster.lib.dfplus.mergerule import MergeRule
from caster.lib.dfplus.state.actions2 import NullAction


class AliasesNon(MergeRule):
    mapping = {
        "default command":       NullAction(), 
        }

class Aliases(MergeRule):
    non = AliasesNon
    
    MESSAGE_SPLITTER = "<chain_alias>"
    LINE_PATTERN = re.compile(r"'([\w ]+)':[ ]{0,1}Text\('(.*)'\)")
    
    mapping = {
        "default command":       NullAction(), 
        }