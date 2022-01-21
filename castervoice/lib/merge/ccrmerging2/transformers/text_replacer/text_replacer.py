from dragonfly.grammar.elements import Choice

from castervoice.lib import printer
from castervoice.lib.merge.ccrmerging2.transformers.base_transformer import BaseRuleTransformer
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_extra_data import TextReplacementExtraData
from castervoice.lib.merge.ccrmerging2.transformers.text_replacer.tr_parser import TRParser


def _analyze_extras(spec):
    """
    Takes a spec and returns a list of extras and whether they're required or not.
    """
    extras_data = []

    angles_mode = False
    brackets_mode = False
    current_extra_name = ""
    for character in spec:
        if character == '[':
            brackets_mode = True
            continue
        if character == ']':
            brackets_mode = False
            continue
        if character == '<':
            angles_mode = True
            continue
        if character == '>':
            angles_mode = False
            extras_data.append(TextReplacementExtraData(current_extra_name, not brackets_mode))
            current_extra_name = ""  # reset for next
            continue
        if angles_mode:
            current_extra_name += character

    return extras_data


def _detect_illegal_spec_alteration(extra_analyses, new_spec):
    for extra_data in extra_analyses:
        if extra_data.required and "<{}>".format(extra_data.name) not in new_spec:
            return extra_data
    return None


def _spec_override_from_config(rule, definitions):
    '''redundant safety check'''
    if len(definitions) == 0:
        return rule

    '''SPECS'''
    mapping = rule._mapping.copy()
    specs_changed = False
    for spec in list(mapping.keys()):
        action = mapping[spec]

        extra_analyses = _analyze_extras(spec)

        new_spec = spec
        for token_to_replace in definitions.specs.keys():
            if token_to_replace in new_spec:
                replacement = definitions.specs[token_to_replace]
                new_spec = new_spec.replace(token_to_replace, replacement)

        if spec == new_spec:
            continue

        '''
        We want to protect the user from:
        - removing required extras from specs
        - accidentally renaming required extras
        But we still want the user to be able to:
        - move required extras
        - remove optional extras
        '''
        violation = _detect_illegal_spec_alteration(extra_analyses, new_spec)
        if violation is not None:
            printer.out("Illegal spec modification: cannot alter required extras. " +
                        "Cannot modify <{}> in \"{}\".".format(violation.name, spec))
            continue

        del mapping[spec]
        mapping[new_spec] = action
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
            if isinstance(value, str):
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
            if len(self._definitions) > 0:
                printer.out("Text replacing transformer from file 'words.txt' activated ...")
        except Exception:
            printer.out("Unable to parse words.txt")

    def get_pronunciation(self):
        return "text replacer"

    def _transform(self, rule):
        return _spec_override_from_config(rule, self._definitions)

    def _is_applicable(self, rule):
        return True


def get_transformer():
    return TextReplacerTransformer
