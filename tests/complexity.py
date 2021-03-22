'''
Created on Oct 10, 2015

@author: synkarius
'''
import io
import random
import re
import time
from builtins import str

from dragonfly.grammar.elements import Choice
from dragonfly.grammar.grammar_base import Grammar

from castervoice.lib import settings
from castervoice.lib.actions import Text
from castervoice.rules.core.alphabet_rules.alphabet import Alphabet
from castervoice.rules.core.navigation_rules.nav import Navigation
from castervoice.rules.core.keyboard_rules.keyboard import Keyboard
from castervoice.rules.core.numbers_rules.numeric import Numbers
from castervoice.rules.core.punctuation_rules.punctuation import Punctuation
from castervoice.rules.ccr.python_rules.python import Python
from castervoice.lib.merge.ccrmerger_legacy import CCRMerger # Deprecated
from castervoice.lib.merge.merge.mergepair import MergeInf # Deprecated
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


def _report_to_file(message, path=None):
    _path = settings.SETTINGS["paths"]["LOG_PATH"]
    if path is not None: _path = path
    with io.open(_path, 'at', encoding="utf-8") as f:
        f.write(str(message) + "\n")


def get_500_words():
    return [
        "basin", "return", "picture", "unequaled", "drop", "nonstop", "protective",
        "ancient", "moldy", "cry", "weigh", "drip", "tow", "cover", "fat", "unsightly",
        "shade", "puncture", "scissors", "sun", "gamy", "fry", "rabbit", "embarrassed",
        "ahead", "impress", "answer", "truck", "aloof", "illustrious", "cave", "pumped",
        "angle", "economic", "knowledgeable", "fuel", "drum", "swim", "scarf", "offer",
        "vigorous", "sad", "vessel", "cats", "exercise", "sophisticated", "interest",
        "changeable", "melt", "woozy", "fertile", "light", "bee", "stomach", "panicky",
        "pump", "stranger", "plucky", "grubby", "black-and-white", "afraid",
        "descriptive", "house", "jolly", "clammy", "wary", "detail", "grain", "analyse",
        "zippy", "polish", "verdant", "surround", "scientific", "functional", "place",
        "detect", "undress", "baseball", "general", "sleep", "oranges", "correct", "walk",
        "wreck", "rinse", "thought", "hall", "receipt", "massive", "include", "marvelous",
        "futuristic", "telling", "soft", "nest", "insidious", "curvy", "outstanding",
        "driving", "elastic", "stew", "crow", "selection", "roll", "debonair", "hand",
        "country", "languid", "ball", "monkey", "flow", "clever", "seed", "coherent",
        "match", "scare", "tree", "butter", "draconian", "flower", "untidy", "annoying",
        "fruit", "upset", "whip", "sneeze", "enormous", "arithmetic", "trashy", "bushes",
        "unknown", "nutritious", "sudden", "consist", "bone", "occur", "guide", "eager",
        "strong", "frightening", "church", "nice", "middle", "time", "wicked", "health",
        "cultured", "crack", "ill", "advice", "mine", "meeting", "toys", "silent", "part",
        "lively", "threatening", "talented", "wax", "unusual", "profuse", "true", "lucky",
        "lighten", "piquant", "spoon", "screw", "creepy", "gusty", "week", "pot", "scene",
        "unsuitable", "cakes", "flag", "recondite", "earth", "prick", "robin", "separate",
        "paper", "receive", "meaty", "plane", "flash", "grotesque", "arrest", "reading",
        "stimulating", "spurious", "pocket", "woebegone", "imported", "far-flung", "wood",
        "stroke", "grieving", "clip", "knit", "frame", "cracker", "prose", "carry",
        "watch", "stop", "earn", "end", "married", "night", "obsequious", "tooth",
        "range", "jar", "lush", "quickest", "shivering", "fearful", "reflect",
        "agonizing", "great", "spare", "jam", "dizzy", "rely", "smoggy", "argue", "pull",
        "glow", "unequal", "torpid", "optimal", "breakable", "thread", "satisfy",
        "blushing", "pollution", "capable", "gold", "suffer", "store", "false",
        "maddening", "zip", "sister", "wry", "anger", "fear", "intend", "eatable",
        "magenta", "hope", "shaggy", "pathetic", "bite", "honorable", "shave", "trail",
        "noisy", "cheese", "spot", "legal", "oatmeal", "porter", "curve", "wrathful",
        "wiry", "fix", "sofa", "dust", "lake", "aquatic", "bored", "slimy", "infamous",
        "nest", "beds", "cooperative", "zealous", "crayon", "produce", "market", "three",
        "dispensable", "earsplitting", "helpless", "switch", "memory", "rich", "absorbed",
        "sore", "representative", "preserve", "depend", "careless", "science", "train",
        "eggs", "expansion", "volleyball", "learn", "free", "trouble", "salty", "spotted",
        "branch", "approve", "concentrate", "pointless", "shop", "shame", "remove",
        "protect", "disagreeable", "kill", "territory", "lumpy", "gabby", "behavior",
        "maniacal", "mate", "pale", "knot", "abrupt", "applaud", "tangible", "mourn",
        "abounding", "amuse", "part", "deer", "class", "fire", "picayune", "suspect",
        "borrow", "squealing", "late", "lonely", "proud", "pass", "material", "broad",
        "harbor", "veil", "absurd", "trot", "advise", "noiseless", "land", "zany",
        "entertain", "good", "recognise", "uninterested", "school", "connect", "watch",
        "towering", "filthy", "day", "invent", "complex", "tip", "frogs", "refuse",
        "reaction", "room", "icicle", "sin", "awesome", "disgusting", "pretty",
        "instinctive", "mouth", "toad", "hesitant", "basket", "volatile", "dinner",
        "sniff", "road", "trousers", "accidental", "miss", "morning", "weight",
        "condemned", "youthful", "advertisement", "finicky", "dramatic", "radiate",
        "shelter", "floor", "toe", "burly", "instruct", "unable", "venomous", "poison",
        "drop", "airport", "cough", "wool", "pat", "ticket", "shape", "efficient", "eye",
        "flimsy", "voice", "surprise", "treatment", "sound", "panoramic", "domineering",
        "trace", "square", "curious", "uppity", "crush", "teaching", "ants", "fool",
        "outgoing", "testy", "double", "pear", "man", "striped", "tasty", "mask",
        "marble", "hard", "unadvised", "effect", "screeching", "hope", "canvas",
        "redundant", "men", "cabbage", "club", "sock", "hot", "sassy", "passenger",
        "admire", "cub", "home", "workable", "dapper", "cruel", "toothbrush", "credit",
        "cloudy", "plant", "psychedelic", "spicy", "strange", "dashing", "design",
        "abusive", "shirt", "care", "drunk", "cooing", "smoke", "muddled", "festive",
        "useful", "raspy", "vegetable", "peace", "tangy", "grease", "plan", "lettuce",
        "hook", "transport", "milk", "exciting", "license", "back", "turn", "yummy",
        "secretive", "measure", "salt", "delicate", "greedy", "spotless", "mark", "rain",
        "fascinated", "harsh", "abaft", "versed", "sheet"
    ]


def get_random_int():
    return random.randint(1, 100000)


def get_giant_choice(name):
    choices = {}
    for word in get_500_words():
        choices[word] = get_random_int()
    return Choice(name, choices)


class ComplexityTestRule(MergeRule):

    pronunciation = "complexity"

    def __init__(self, num_choice_500s, num_specs):

        mapping = {}
        extras = []
        defaults = {}

        w500 = get_500_words()
        spec_base = ""
        text_base = ""

        for k in range(0, num_choice_500s):
            extra_name = "giant_" + str(k)
            spec_base += " <" + extra_name + ">"
            text_base += " %(" + extra_name + ")s"
            extras.append(get_giant_choice(extra_name))

        for i in range(0, num_specs):
            word = w500[i]
            mapping[word + spec_base] = R(Text(word + text_base), show=False)

        MergeRule.__init__(
            self,
            name="complexity test",
            mapping=mapping,
            extras=extras,
            defaults=defaults)


def core_and_python():
    '''intended to mimic the average use case: '''
    return [Alphabet(), Navigation(), Numbers(), Punctuation(), Keyboard(), Python()]


def prep_merger(merger, nc, ns):
    ctr = ComplexityTestRule(nc, ns)
    for rule in core_and_python() + [ctr]:
        merger.add_global_rule(rule)
    merger.update_config()
    merger.merge(MergeInf.BOOT)


def prep_grammar(grammar, nc, ns):
    ctr = ComplexityTestRule(nc, ns)
    for rule in core_and_python() + [ctr]:
        grammar.add_rule(rule)


class Result(object):
    def __init__(self, report, choices, specs, elements, ccr_max, broke):
        self.report = report
        self.choices = choices
        self.specs = specs
        self.elements = elements
        self.ccr_max = ccr_max
        self.broke = broke


def test(specs, choices, ccr_max):
    broke = False

    print("creating complexity test: \n"\
                     +str(specs)+" specs \n"\
                     +str(choices)+" Choice-500s \n"\
                     +str(ccr_max) + " ccr max" )

    grammar = Grammar("test " + str(int(time.time())))
    print(grammar)
    '''set up realistic scenario'''
    merger = CCRMerger(False)
    prep_grammar(grammar, choices, specs)
    prep_merger(merger, choices, specs)

    report = grammar.get_complexity_string()
    print(".")
    '''activate everything except the heavy rule'''
    merger_ccr_activator = merger.global_rule_changer()
    for rule in core_and_python():
        merger_ccr_activator(rule.get_pronunciation(), True, False)
    print("..")
    merger.selfmod_rule_changer()("css", True, False)
    print("...")
    '''activate the heavy rule'''
    try:
        merger_ccr_activator(ComplexityTestRule.pronunciation, True, False)
    except:
        broke = True
    #             reports.append("BadGrammar at "+str(i)+" Choice-500s ; "+str(i)+" specs\n"+report+"\n")
    #             kCUs.append(complexity * ccr_max / 1000)
    m = re.search(r"rules, ([0-9]+) elements", report)
    elements = m.group(1)
    print("... .   e(" + elements + ")")
    '''clean up'''
    merger.wipe()
    for rule in grammar.rules:
        rule.disable()
    grammar.disable()
    del grammar
    print("... ..")

    return Result(report, choices, specs, elements, ccr_max, broke)


def run_tests():
    original_ccr_max = settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"]
    reports = [
        "Caster/Dragonfly Grammar Complexity Report v2\n===============================\n\n"
    ]
    start_time = time.time()
    cycle_count = 1

    for i in range(0, 3):
        if i != 0: settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"] += 1
        ccr_max = settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"] + 2
        print("Run " + str(i + 1) + " /3")

        not_max_yet = True
        nspecs = 2
        nc_orig = 2
        while not_max_yet:

            for nchoices in range(nc_orig, 500, 4):

                result = test(nspecs, nchoices, ccr_max)
                reports.append("\ncycles: "+str(cycle_count)\
                               +" | ccrm: "+str(result.ccr_max)\
                               +" | specs: "+str(result.specs)\
                               +" | choice-500s: "+str(result.choices)\
                               +" | elements: "+str(result.elements)\
                               +" | broke: "+str(result.broke)\
                               +"\n")
                cycle_count += 1
                if result.broke:
                    nspecs += 2

                    reports.append(result.report + "\n")
                    '''if choices max out at 1, the test is over'''
                    if result.choices == nc_orig: not_max_yet = False
                    break

    reports.append("\nSettings toml CCR Max Reps: " + str(original_ccr_max) + "\n")
    reports.append(
        "Total time for test: " + str(int(time.time() - start_time)) + " sec\n\n")
    result = "".join(reports)
    report_path = settings.SETTINGS["paths"]["BASE_PATH"] + "/bin/data/complexity_report_" + str(
        time.time()) + ".txt"
    print("Report saved to " + report_path)
    _report_to_file(result, report_path)

    settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"] = original_ccr_max
