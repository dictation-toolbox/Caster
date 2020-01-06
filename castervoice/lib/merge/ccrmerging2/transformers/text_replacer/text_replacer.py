from dragonfly.grammar.elements import Choice

from castervoice.lib import printer
from castervoice.lib.merge.ccrmerging2.transformers.base_transformer import BaseRuleTransformer
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_item import TRItem
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_parser import TRParser
import six
if six.PY2:
    def zip_longest(*args):
        return map(None, *args)
else:
    from itertools import zip_longest # pylint: disable=no-name-in-module

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
    c = [b for a in zip_longest(q, p.extras) for b in a if b is not None]


    return "".join(c)


def _spec_override_from_config(rule, definitions):
    '''redundant safety check'''
    if len(definitions) == 0:
        return rule

    '''SPECS'''
    mapping = rule._mapping.copy()
    specs_changed = False
    for spec in list(mapping.keys()):
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
    extras_list = list(rule._extras.values())
    resulting_extras_list = list(extras_list)
    extras_changed = False
    for extra in extras_list:
        # only choices; no need to bother with dictation or integers
        if isinstance(extra, Choice):
            choices_dict_copy = extra._choices.copy()  # operate on this copy of the choices dict
            choices_dict_copy_keys = set(choices_dict_copy.keys())
            replaced_a_choice_key = False
            for choices_key in choices_dict_copy_keys:  # ex: "dunce make" = key, something else = value
                for replaceable_text in definitions.extras.keys():  # ex: "dunce" is key, "down" is the value
                    if replaceable_text in choices_key:  # ex: "dunce" is in "dunce make"
                        replaced_a_choice_key = True
                        value = choices_dict_copy[choices_key]
                        del choices_dict_copy[choices_key]
                        replacement = definitions.extras[replaceable_text]
                        choices_key = choices_key.replace(replaceable_text, replacement)
                        choices_dict_copy[choices_key] = value
            if replaced_a_choice_key:
                extras_changed = True
                new_choice = Choice(extra.name, choices_dict_copy)
                resulting_extras_list.remove(extra)
                resulting_extras_list.append(new_choice)

    '''DEFAULTS'''
    defaults = rule._defaults.copy()
    defaults_changed = False
    if len(defaults) > 0:
        for default_key in list(defaults.keys()):  #
            value = defaults[default_key]
            if isinstance(value, six.string_types):
                '''only replace strings; also,
                only replace values, not keys:
                default_key should not be changed - it will never be spoken'''
                nvalue = value  # new value
                replaced_a_choice_key = False
                for old in definitions.defaults.keys():  # 'old' is the target word(s) in the old 'value'
                    new = definitions.defaults[old]
                    if old in nvalue:
                        nvalue = nvalue.replace(old, new)
                        replaced_a_choice_key = True
                if replaced_a_choice_key:
                    defaults[default_key] = nvalue
                    defaults_changed = True

    if specs_changed or extras_changed or defaults_changed:
        # rule_class = rule.__class__
        rule.__init__(name=rule.name,
                      mapping=mapping,
                      extras=resulting_extras_list,
                      defaults=defaults)
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
