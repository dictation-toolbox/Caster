################################# Global Filter Functions From File module  ############################################
'''GlobalFilterDefs overrides ALL instances of some word(s) in all rules'''

import io
import os

from castervoice.lib import settings
from castervoice.lib.dfplus.merge.mergepair import MergeInf, MergePair
from dragonfly.grammar.elements import Choice


class PreservedSpec(object):
    def __init__(self):
        self.original = None  # original spec from Caster
        self.extras = []  # bound extras' words
        self.cleaned = None  # original with bound extras replaced with '?'s
        self.altered = None  # 'cleaned' after replacement process

    @staticmethod
    def preserve(spec):
        p = PreservedSpec()
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


class GlobalFilterDefs(object):

    P = "<?>"

    @staticmethod
    def preserve(spec, target):
        _ = "<" + target + ">"
        if _ in spec:
            return spec.replace(_, GlobalFilterDefs.P)
        else:
            return spec

    @staticmethod
    def restore(spec, target):
        return spec.replace(GlobalFilterDefs.P, "<" + target + ">")

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

            if original in GlobalFilterDefs.MODES:
                mode = GlobalFilterDefs.MODES[original]
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


DEFS = None

if os.path.isfile(settings.SETTINGS["paths"]["SIMPLIFIED_FILTER_RULES_PATH"]):
    '''User must create or place words.txt in '.caster\filters' folder for it to get picked up here'''
    with io.open(settings.SETTINGS["paths"]["SIMPLIFIED_FILTER_RULES_PATH"],
                 "rt",
                 encoding="utf-8") as f:
        lines = f.readlines()
        try:
            DEFS = GlobalFilterDefs(lines)
        except Exception:
            print("Unable to parse words.txt")


def spec_override_from_config(mp):
    '''run at boot time only: changes are permanent'''
    if mp.time != MergeInf.BOOT_NO_MERGE:  # 3 == MergeInf.BOOT
        return
    '''redundant safety check'''
    if DEFS is None:
        return

    for rule in [mp.rule1, mp.rule2]:
        if rule is not None:
            '''SPECS'''
            specs_changed = False
            for spec in rule.mapping_actual().keys():
                action = rule.mapping_actual()[spec]

                pspec = PreservedSpec.preserve(spec)

                for original in DEFS.specs.keys():
                    if original in pspec.altered:
                        new = DEFS.specs[original]
                        pspec.altered = pspec.altered.replace(original, new)

                pspec.altered = PreservedSpec.restore(pspec)

                if spec == pspec.altered:
                    continue

                del rule.mapping_actual()[spec]
                rule.mapping_actual()[pspec.altered] = action
                specs_changed = True
            '''EXTRAS'''
            extras = rule.extras_copy().values()
            extras_changed = False
            if len(extras) > 0:
                replacements = {}
                for extra in extras:
                    if isinstance(extra,
                                  Choice):  # IntegerRefSTs will be dealt with elsewhere
                        choices = extra._choices
                        replace = False
                        for s in choices.keys(
                        ):  #ex: "dunce make" is key, some int or whatever is the value
                            for ns in DEFS.extras.keys(
                            ):  #ex: "dunce" is key, "down" is the value
                                if ns in s:  # ex: "dunce" is in "dunce make"
                                    replace = True
                                    val = choices[s]
                                    del choices[s]
                                    s = s.replace(ns, DEFS.extras[ns])
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
            defaults = rule.defaults_copy()
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
                        for old in DEFS.defaults.keys(
                        ):  # 'old' is the target word(s) in the old 'value'
                            new = DEFS.defaults[old]
                            if old in nvalue:
                                nvalue = nvalue.replace(old, new)
                                replace = True
                        if replace:
                            defaults[default_key] = nvalue
                            defaults_changed = True

            if specs_changed or extras_changed or defaults_changed:
                rule.__init__(rule._name, rule.mapping_actual(), extras, defaults,
                              rule._exported, rule.ID, rule.composite, rule.compatible,
                              rule._mcontext, rule._mwith)


if DEFS is not None:
    print("Global simplified rule filter 'words.txt' activated...")


def run_on(rule):
    if DEFS is not None:
        mp = MergePair(MergeInf.BOOT_NO_MERGE, MergeInf.GLOBAL, None, rule, False)
        spec_override_from_config(mp)
