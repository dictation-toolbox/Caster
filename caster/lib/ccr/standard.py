'''
Created on Oct 17, 2015

@author: synkarius
'''
class SymbolSpecs(object):
    IF = "if"
    ELSE = "else"
    ELIF = "elif"
    
    SWITCH = "switch"
    CASE = "case of"
    BREAK = "break"
    DEFAULT = "default case"
    
    DO_LOOP = "do loop"
    WHILE_LOOP = "while"
    FOR_LOOP = "for o"
    FOR_EACH_LOOP = "for each"
    
    TO_INTEGER = "to integer"
    TO_FLOAT = "to float"
    TO_STRING = "to string"
    
    AND = "lodge and"
    OR = "lodge or"
    NOT = "lodge not"
    
    SYSOUT = "print out"
    
    IMPORT = "import"
    
    FUNCTION = "function"
    CLASS = "class"
    
    COMMENT = "add comment"
    LONG_COMMENT = "long comment"
    
    NULL = "newell"
    
    RETURN = "return"
    
    TRUE = "true"
    FALSE = "false"

    ARROW = "row"

    # not part of the programming standard:
    CANCEL = "(cape | escape)"
    
    @staticmethod
    def set_cancel_word(spec):
        SymbolSpecs.CANCEL = spec
