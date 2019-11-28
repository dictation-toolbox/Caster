'''
Created on Oct 17, 2015

@author: synkarius
'''


class SymbolSpecs(object):
    IF = "iffae"
    ELSE = "shells"

    SWITCH = "switch"
    CASE = "case of"
    BREAK = "breaker"
    DEFAULT = "default"

    DO_LOOP = "do loop"
    WHILE_LOOP = "while loop"
    FOR_LOOP = "for loop"
    FOR_EACH_LOOP = "for each"

    TO_INTEGER = "convert to integer"
    TO_FLOAT = "convert to floating point"
    TO_STRING = "convert to string"

    AND = "lodge and"
    OR = "lodge or"
    NOT = "lodge not"

    SYSOUT = "print to console"

    IMPORT = "import"

    FUNCTION = "function"
    CLASS = "class"

    COMMENT = "add comment"
    LONG_COMMENT = "long comment"

    NULL = "value not"

    RETURN = "return"

    TRUE = "value true"
    FALSE = "value false"

    # not part of the programming standard:
    CANCEL = "(terminate | escape | exit | cancel)"

    @staticmethod
    def set_cancel_word(spec):
        SymbolSpecs.CANCEL = spec
