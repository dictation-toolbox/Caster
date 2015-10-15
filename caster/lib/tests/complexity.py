'''
Created on Oct 10, 2015

@author: synkarius
'''
import random
import re
import time

from dragonfly.actions.action_text import Text
from dragonfly.grammar.elements import Choice
from dragonfly.grammar.grammar_base import Grammar

from caster.lib import utilities, settings
from caster.lib.ccr.core.alphabet import Alphabet
from caster.lib.ccr.core.nav import Navigation
from caster.lib.ccr.core.numbers import Numbers
from caster.lib.ccr.core.punctuation import Punctuation
from caster.lib.ccr.python.python import Python
from caster.lib.dfplus.hint.hintnode import NodeRule
from caster.lib.dfplus.hint.nodes import css
from caster.lib.dfplus.merge.ccrmerger import CCRMerger, Inf
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


def get_500_words():
    return ["basin","return","picture","unequaled","drop","nonstop","protective","ancient","moldy","cry","weigh","drip","tow","cover","fat","unsightly",
            "shade","puncture","scissors","sun","gamy","fry","rabbit","embarrassed","ahead","impress","answer","truck","aloof","illustrious","cave","pumped",
            "angle","economic","knowledgeable","fuel","drum","swim","scarf","offer","vigorous","sad","vessel","cats","exercise","sophisticated","interest",
            "changeable","melt","woozy","fertile","light","bee","stomach","panicky","pump","stranger","plucky","grubby","black-and-white","afraid",
            "descriptive","house","jolly","clammy","wary","detail","grain","analyse","zippy","polish","verdant","surround","scientific","functional",
            "place","detect","undress","baseball","general","sleep","oranges","correct","walk","wreck","rinse","thought","hall","receipt","massive",
            "include","marvelous","futuristic","telling","soft","nest","insidious","curvy","outstanding","driving","elastic","stew","crow","selection",
            "roll","debonair","hand","country","languid","ball","monkey","flow","clever","seed","coherent","match","scare","tree","butter","draconian",
            "flower","untidy","annoying","fruit","upset","whip","sneeze","enormous","arithmetic","trashy","bushes","unknown","nutritious","sudden","consist",
            "bone","occur","guide","eager","strong","frightening","church","nice","middle","time","wicked","health","cultured","crack","ill","advice","mine",
            "meeting","toys","silent","part","lively","threatening","talented","wax","unusual","profuse","true","lucky","lighten","piquant","spoon","screw",
            "creepy","gusty","week","pot","scene","unsuitable","cakes","flag","recondite","earth","prick","robin","separate","paper","receive","meaty","plane",
            "flash","grotesque","arrest","reading","stimulating","spurious","pocket","woebegone","imported","far-flung","wood","stroke","grieving","clip",
            "knit","frame","cracker","prose","carry","watch","stop","earn","end","married","night","obsequious","tooth","range","jar","lush","quickest",
            "shivering","fearful","reflect","agonizing","great","spare","jam","dizzy","rely","smoggy","argue","pull","glow","unequal","torpid","optimal",
            "breakable","thread","satisfy","blushing","pollution","capable","gold","suffer","store","false","maddening","zip","sister","wry","anger","fear"
            ,"intend","eatable","magenta","hope","shaggy","pathetic","bite","honorable","shave","trail","noisy","cheese","spot","legal","oatmeal","porter",
            "curve","wrathful","wiry","fix","sofa","dust","lake","aquatic","bored","slimy","infamous","nest","beds","cooperative","zealous","crayon",
            "produce","market","three","dispensable","earsplitting","helpless","switch","memory","rich","absorbed","sore","representative","preserve",
            "depend","careless","science","train","eggs","expansion","volleyball","learn","free","trouble","salty","spotted","branch","approve",
            "concentrate","pointless","shop","shame","remove","protect","disagreeable","kill","territory","lumpy","gabby","behavior","maniacal",
            "mate","pale","knot","abrupt","applaud","tangible","mourn","abounding","amuse","part","deer","class","fire","picayune","suspect","borrow",
            "squealing","late","lonely","proud","pass","material","broad","harbor","veil","absurd","trot","advise","noiseless","land","zany","entertain",
            "good","recognise","uninterested","school","connect","watch","towering","filthy","day","invent","complex","tip","frogs","refuse","reaction",
            "room","icicle","sin","awesome","disgusting","pretty","instinctive","mouth","toad","hesitant","basket","volatile","dinner","sniff","road",
            "trousers","accidental","miss","morning","weight","condemned","youthful","advertisement","finicky","dramatic","radiate","shelter","floor",
            "toe","burly","instruct","unable","venomous","poison","drop","airport","cough","wool","pat","ticket","shape","efficient","eye","flimsy",
            "voice","surprise","treatment","sound","panoramic","domineering","trace","square","curious","uppity","crush","teaching","ants","fool",
            "outgoing","testy","double","pear","man","striped","tasty","mask","marble","hard","unadvised","effect","screeching","hope","canvas",
            "redundant","men","cabbage","club","sock","hot","sassy","passenger","admire","cub","home","workable","dapper","cruel","toothbrush",
            "credit","cloudy","plant","psychedelic","spicy","strange","dashing","design","abusive","shirt","care","drunk","cooing","smoke","muddled"
            ,"festive","useful","raspy","vegetable","peace","tangy","grease","plan","lettuce","hook","transport","milk","exciting","license","back"
            ,"turn","yummy","secretive","measure","salt","delicate","greedy","spotless","mark","rain","fascinated","harsh","abaft","versed","sheet"]

def get_random_int():
    return random.randint(1, 100000)

def get_giant_choice(name):
    choices = {}
    for word in get_500_words():
        choices[word] = get_random_int()
    return Choice(name,choices)

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
            extra_name = "giant_"+str(k)
            spec_base += " <"+extra_name+">"
            text_base += " %("+extra_name+")s"
            extras.append(get_giant_choice(extra_name))
        
        for i in range(0, num_specs):
            word = w500[i]
            mapping[word+spec_base] = R(Text(word+text_base), show=False)
        
        MergeRule.__init__(self, name="complexity test", mapping=mapping, extras=extras, defaults=defaults)

def core_and_python():
    '''intended to mimic the average use case: '''
    return [Alphabet(), Navigation(), Numbers(), Punctuation(), Python()]

def prep_merger(merger, nc, ns):
    ctr = ComplexityTestRule(nc, ns)
    css_ = NodeRule(css.getCSSNode(), None)
    for rule in core_and_python()+[ctr]:
        merger.add_global_rule(rule)
    merger.add_selfmodrule(css_)
    merger.update_config()
    merger.merge(Inf.BOOT)

def prep_grammar(grammar, nc, ns):
    ctr = ComplexityTestRule(nc, ns)
    css_ = NodeRule(css.getCSSNode(), None)
    for rule in core_and_python()+[ctr]:
        grammar.add_rule(rule)
    grammar.add_rule(css_)



def run_tests():
    starting_level = 1
    original_ccr_max = settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"]
    kCUs = []
    reports = ["Caster/Dragonfly Grammar Complexity Report\n===============================\n\n"]
    start_time = time.time()
    
    for k in range(0, 3):
        if k != 0:
            settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"] += 1
        ccr_max = settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"] + 2
        broke = False
        
        print "Run "+str(k+1)+" /3"
        for i in range(starting_level, 500):
            print "creating complexity test: "+str(i)+" Choice-500s ; "+str(i)+" specs ; " +str(ccr_max) + " ccr max" 
            grammar = Grammar("test "+str(int(time.time())))
            print grammar
            merger = CCRMerger(False)
            prep_grammar(grammar, i, i)
            report = grammar.get_complexity_string()
            prep_merger(merger, i, i)
            merger_ccr_activator = merger.global_rule_changer()
            print "."
            for rule in core_and_python():
                merger_ccr_activator(rule.get_name(), True, False)
                merger.node_rule_changer()("css", True, False)
            print ".."
            try:
                merger_ccr_activator(ComplexityTestRule.pronunciation, True, False)
            except:
                broke = True
                reports.append("BadGrammar at "+str(i)+" Choice-500s ; "+str(i)+" specs\n"+report+"\n")
                m = re.search(r"rules, ([0-9]+) elements", report)
                complexity = int(m.group(1))
                kCUs.append(complexity * ccr_max / 1000)
            print "..."
            merger.wipe()
            print "... ."
            
            for rule in grammar.rules: rule.disable()
            grammar.disable()
            del grammar
            
            print "... .."
            if broke: break
    
    avg_kcus = (kCUs[0]+kCUs[1]+kCUs[2])/3
    reports.append("\nCCR Max Reps: "+str(original_ccr_max)+"\n")
    reports.append("Total time for test: "+str(int(time.time()-start_time))+" sec\n\n")
    result = "".join(reports)
    report_path = settings.SETTINGS["paths"]["BASE_PATH"] + "/bin/data/complexity_report_"+str(time.time())+".txt"
    print "Report saved to "+report_path
    settings.report_to_file(result, report_path)
    
    
    settings.SETTINGS["miscellaneous"]["max_ccr_repetitions"] = original_ccr_max