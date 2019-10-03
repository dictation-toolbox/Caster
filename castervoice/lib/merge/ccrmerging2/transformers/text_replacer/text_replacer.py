from dragonfly.grammar.elements import Choice

from castervoice.lib import printer
from castervoice.lib.merge.ccrmerging2.transformers.base_transformer import BaseRuleTransformer
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_item import TRItem
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_parser import TRParser


def _preserve(spec):
    p = TRItem()
    p.original = spec

    angles_mode = False
    preserved_word = ""
    cleaned_spec = ""
    for c in spec:
        if c == '<':
            angles_mode = True
            cleaned_spec += "<?"
            continue
        elif c == '>':
            angles_mode = False
            p.extras.append(preserved_word)
            preserved_word = ""
            cleaned_spec += ">"
            continue
        elif angles_mode:
            preserved_word += c
        else:
            cleaned_spec += c
    p.cleaned = cleaned_spec
    p.altered = cleaned_spec

    return p


def _restore(pspec):
    p = pspec

    q = p.altered.split("?")
    if len(q) == 1:  # no bound extras
        return p.altered  # so just return the result

    # intersperse the lists
    c = [b for a in map(None, q, p.extras) for b in a if b is not None]

    return "".join(c)


def _spec_override_from_config(rule, definitions):
    '''redundant safety check'''
    if len(definitions) == 0:
        return rule

    mapping = rule._mapping.copy()
    extras = rule._extras.copy()
    defaults = rule._defaults.copy()

    '''SPECS'''
    specs_changed = False
    for spec in mapping.keys():
        action = mapping[spec]

        pspec = _preserve(spec)

        for original in definitions.specs.keys():
            if original in pspec.altered:
                new = definitions.specs[original]
                pspec.altered = pspec.altered.replace(original, new)

        pspec.altered = _restore(pspec)

        if spec == pspec.altered:
            continue

        del mapping[spec]
        mapping[pspec.altered] = action
        specs_changed = True

    '''EXTRAS'''
    extras_values = extras.values()
    extras_changed = False
    if len(extras_values) > 0:
        replacements = {}
        for extra in extras_values:
            if isinstance(extra, Choice):  # IntegerRefSTs will be dealt with elsewhere
                choices = extra._choices
                replace = False
                for s in choices.keys():  # ex: "dunce make" is key, some int or whatever is the value
                    for ns in definitions.extras.keys():  # ex: "dunce" is key, "down" is the value
                        if ns in s:  # ex: "dunce" is in "dunce make"
                            replace = True
                            val = choices[s]
                            del choices[s]
                            s = s.replace(ns, definitions.extras[ns])
                            choices[s] = val
                if replace:
                    new_choice = Choice(extra.name, choices)
                    replacements[extra] = new_choice
        for old_choice in replacements:
            new_choice = replacements[old_choice]
            extras_values.remove(old_choice)
            extras_values.append(new_choice)
        if len(replacements) > 0:
            extras_changed = True

    '''DEFAULTS'''
    defaults_changed = False
    if len(defaults) > 0:
        for default_key in defaults.keys():  #
            value = defaults[default_key]
            if isinstance(value, basestring):
                '''only replace strings; also,
                only replace values, not keys:
                default_key should not be changed - it will never be spoken'''
                nvalue = value  # new value
                replace = False
                for old in definitions.defaults.keys():  # 'old' is the target word(s) in the old 'value'
                    new = definitions.defaults[old]
                    if old in nvalue:
                        nvalue = nvalue.replace(old, new)
                        replace = True
                if replace:
                    defaults[default_key] = nvalue
                    defaults_changed = True

    if specs_changed or extras_changed or defaults_changed:
        # rule_class = rule.__class__
        rule.__init__(name=rule.name,
                      mapping=mapping,
                      extras=extras_values,
                      defaults=defaults,
                      exported=rule._exported)
    return rule


class TextReplacerTransformer(BaseRuleTransformer):

    def __init__(self, parser=TRParser):
        try:
            parser_instance = parser()
            self._definitions = parser_instance.create_definitions()
        except Exception:
            printer.out("Unable to parse words.txt")
        if len(self._definitions) > 0:
            printer.out("Text replacing transformer from file 'words.txt' activated ...")

    def get_pronunciation(self):
        return "text replacer"

    def _transform(self, rule):
        return _spec_override_from_config(rule, self._definitions)

    def _is_applicable(self, rule):
        return True


def get_transformer():
    return TextReplacerTransformer
