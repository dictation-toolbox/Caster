import io
import os

from dragonfly.grammar.elements import Choice

from castervoice.lib import settings
from castervoice.lib.dfplus.ccrmerging2.transformers.base_transformer import BaseRuleTransformer

'''
This module defines a global transformer, the parameters of
which are defined in settings.SETTINGS["paths"]["FILTER_DEFS_PATH"]
'''


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


class _GlobalFilterDefs(object):
    P = "<?>"

    @staticmethod
    def preserve(spec, target):
        _ = "<" + target + ">"
        if _ in spec:
            return spec.replace(_, _GlobalFilterDefs.P)
        else:
            return spec

    @staticmethod
    def restore(spec, target):
        return spec.replace(_GlobalFilterDefs.P, "<" + target + ">")

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

            if line.startswith(
                    "#") or not line.strip():  # ignore comments and empty lines
                continue

            pair = line.split("->")
            original = pair[0].strip()

            if original in _GlobalFilterDefs.MODES:
                mode = _GlobalFilterDefs.MODES[original]
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


_DEFS = None


def _load_definitions():
    if os.path.isfile(settings.SETTINGS["paths"]["FILTER_DEFS_PATH"]):
        '''user must create castervoice/user/fdefs.txt for it to get picked up here'''
        with io.open(
                settings.SETTINGS["paths"]["FILTER_DEFS_PATH"], "rt", encoding="utf-8") as f:
            lines = f.readlines()
            try:
                _DEFS = _GlobalFilterDefs(lines)
            except Exception:
                print("Unable to parse words.txt")


def _spec_override_from_config(mergerule):
    '''redundant safety check'''
    if _DEFS is None:
        return

    '''SPECS'''
    specs_changed = False
    for spec in mergerule.mapping_actual().keys():
        action = mergerule.mapping_actual()[spec]

        pspec = _PreservedSpec.preserve(spec)

        for original in _DEFS.specs.keys():
            if original in pspec.altered:
                new = _DEFS.specs[original]
                pspec.altered = pspec.altered.replace(original, new)

        pspec.altered = _PreservedSpec.restore(pspec)

        if spec == pspec.altered:
            continue

        del mergerule.mapping_actual()[spec]
        mergerule.mapping_actual()[pspec.altered] = action
        specs_changed = True
    '''EXTRAS'''
    extras = mergerule.extras_copy().values()
    extras_changed = False
    if len(extras) > 0:
        replacements = {}
        for extra in extras:
            if isinstance(extra,
                          Choice):  # IntegerRefSTs will be dealt with elsewhere
                choices = extra._choices
                replace = False
                for s in choices.keys(
                ):  # ex: "dunce make" is key, some int or whatever is the value
                    for ns in _DEFS.extras.keys(
                    ):  # ex: "dunce" is key, "down" is the value
                        if ns in s:  # ex: "dunce" is in "dunce make"
                            replace = True
                            val = choices[s]
                            del choices[s]
                            s = s.replace(ns, _DEFS.extras[ns])
                            choices[s] = val
                if replace:
                    new_choice = Choice(extra.name, choices)
                    replacements[extra] = new_choice
        for old_choice in replacements:
            new_choice = replacements[old_choice]
            extras.remove(old_choice)
            extras.append(new_choice)
        if len(replacements) > 0:
            extras_changed = True
    '''DEFAULTS'''
    defaults = mergerule.defaults_copy()
    defaults_changed = False
    if len(defaults) > 0:
        replacements = {}
        for default_key in defaults.keys():  #
            value = defaults[default_key]
            if isinstance(value, basestring):
                '''only replace strings; also,
                only replace values, not keys:
                default_key should not be changed - it will never be spoken'''
                nvalue = value  # new value
                replace = False
                for old in _DEFS.defaults.keys(
                ):  # 'old' is the target word(s) in the old 'value'
                    new = _DEFS.defaults[old]
                    if old in nvalue:
                        nvalue = nvalue.replace(old, new)
                        replace = True
                if replace:
                    defaults[default_key] = nvalue
                    defaults_changed = True

    if specs_changed or extras_changed or defaults_changed:
        mergerule.__init__(mergerule._name, mergerule.mapping_actual(), extras, defaults,
                           mergerule._exported, mergerule.ID, mergerule.composite, mergerule.compatible,
                           mergerule._mcontext, mergerule._mwith)
    return mergerule


_load_definitions()
if _DEFS is not None:
    print("Global rule filter from file 'words.txt' activated ...")

'''TODO: make sure this finds its way into both modes of the new merger'''


class GlobalDefinitionsRuleTransformer(BaseRuleTransformer):
    def _transform(self, mergerule):
        return _spec_override_from_config(mergerule)

    def _is_applicable(self, mergerule):
        return True
