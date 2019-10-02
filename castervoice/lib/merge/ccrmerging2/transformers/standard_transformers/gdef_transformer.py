import io
import os

from dragonfly.grammar.elements import Choice

from castervoice.lib import settings, printer
from castervoice.lib.merge.ccrmerging2.transformers.base_transformer import BaseRuleTransformer


class _PreservedSpec(object):
    def __init__(self):
        self.original = None  # original spec from Caster
        self.extras = []  # bound extras' words
        self.cleaned = None  # original with bound extras replaced with '?'s
        self.altered = None  # 'cleaned' after replacement process

    @staticmethod
    def preserve(spec):
        p = _PreservedSpec()
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

    @staticmethod
    def restore(pspec):
        p = pspec

        q = p.altered.split("?")
        if len(q) == 1:  # no bound extras
            return p.altered  # so just return the gfilter result

        # intersperse the lists
        c = [b for a in map(None, q, p.extras) for b in a if b is not None]

        return "".join(c)


class _GlobalFilterDefinitions(object):
    P = "<?>"

    def __len__(self):
        return len(self.specs) + len(self.extras) + len(self.defaults)

    '''parsing modes'''
    MODES = {
        "<<<ANY>>>": 0,
        "<<<SPEC>>>": 1,
        "<<<EXTRA>>>": 2,
        "<<<DEFAULT>>>": 3,
        "<<<NOT_SPECS>>>": 4
    }

    def __init__(self, lines):
        self.specs = {}
        self.extras = {}
        self.defaults = {}
        mode = 0

        for line in lines:

            if line.startswith("#") or not line.strip():  # ignore comments and empty lines
                continue

            pair = line.split("->")
            original = pair[0].strip()

            if original in _GlobalFilterDefinitions.MODES:
                mode = _GlobalFilterDefinitions.MODES[original]
                continue

            new = pair[1].strip()
            new = "#".join(new.split("#")[:1])
            '''only handles mode 1 for now'''
            if mode == 0:
                self.specs[original] = new
                self.extras[original] = new
                self.defaults[original] = new
            elif mode == 1:
                self.specs[original] = new
            elif mode == 2:
                self.extras[original] = new
            elif mode == 3:
                self.defaults[original] = new
            elif mode == 4:
                self.extras[original] = new
                self.defaults[original] = new

    @staticmethod
    def load():
        words_txt_path = settings.settings(["paths", "GDEF_FILE"])
        words_txt_lines = []
        if os.path.isfile(words_txt_path):
            with io.open(words_txt_path, "rt", encoding="utf-8") as f:
                words_txt_lines = f.readlines()
        try:
            return _GlobalFilterDefinitions(words_txt_lines)
        except Exception:
            print("Unable to parse words.txt")


def _spec_override_from_config(rule, definitions):
    '''redundant safety check'''
    if len(definitions) == 0:
        return rule

    mapping = rule._mapping
    extras = rule._extras.copy()
    defaults = rule._defaults.copy()

    '''SPECS'''
    specs_changed = False
    for spec in mapping.keys():
        action = mapping[spec]

        pspec = _PreservedSpec.preserve(spec)

        for original in definitions.specs.keys():
            if original in pspec.altered:
                new = definitions.specs[original]
                pspec.altered = pspec.altered.replace(original, new)

        pspec.altered = _PreservedSpec.restore(pspec)

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
        rule_class = rule.__class__
        rule = rule_class(name=rule.name,
                 mapping=mapping,
                 extras=extras,
                 defaults=defaults,
                 exported=rule._exported)
    return rule


class GlobalDefinitionsRuleTransformer(BaseRuleTransformer):

    def __init__(self):
        self._definitions = _GlobalFilterDefinitions.load()
        if len(self._definitions) > 0:
            printer.out("Global rule filter from file 'words.txt' activated ...")

    def get_pronunciation(self):
        return "global definitions"

    def _transform(self, rule):
        return _spec_override_from_config(rule)

    def _is_applicable(self, rule):
        return True


def get_transformer():
    return GlobalDefinitionsRuleTransformer
