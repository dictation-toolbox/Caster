
from dragonfly import (Grammar, Playback, MappingRule, Key,
                       Dictation, IntegerRef, Function)

from caster.asynch.hmc import vocabulary_processing
from caster.lib import utilities, control, settings
from caster.lib.dfplus.state.short import R
from caster.lib.dfplus.additions import IntegerRefST

def fix_dragon_double():
    try:
        lr = control.nexus().history[len(control.nexus().history) - 1]
        lu = " ".join(lr)
        Key("left/5:" + str(len(lu)) + ", del").execute()
    except Exception:
        utilities.simple_log(False)

class CommandRule(MappingRule):

    mapping = {
        '(lock Dragon | deactivate)':   R(Playback([(["go", "to", "sleep"], 0.0)]), rdescript="Dragon: Go To Sleep"),
        '(number|numbers) mode':        R(Playback([(["numbers", "mode", "on"], 0.0)]), rdescript="Dragon: Number Mode"),
        'spell mode':                   R(Playback([(["spell", "mode", "on"], 0.0)]), rdescript="Dragon: Spell Mode"),
        'dictation mode':               R(Playback([(["dictation", "mode", "on"], 0.0)]), rdescript="Dragon: Dictation Mode"),
        'normal mode':                  R(Playback([(["normal", "mode", "on"], 0.0)]), rdescript="Dragon: Normal Mode"),
        'com on':                       R(Playback([(["command", "mode", "on"], 0.0)]), rdescript="Dragon: Command Mode (On)"),
        'com off':                      R(Playback([(["command", "mode", "off"], 0.0)]), rdescript="Dragon: Command Mode (Off)"),
        'scratch':                      R(Playback([(["scratch", "that"], 0.0)]), rdescript="Dragon: 'Scratch That'"),
        "reboot dragon":                R(Function(utilities.reboot), rdescript="Reboot Dragon Naturallyspeaking"),
        "fix dragon double":            R(Function(fix_dragon_double), rdescript="Fix Dragon Double Letter"),
        "add word to vocabulary":       R(Function(vocabulary_processing.add_vocab), rdescript="Vocabulary Management: Add"),
        "delete word from vocabulary":  R(Function(vocabulary_processing.del_vocab), rdescript="Vocabulary Management: Delete"),
        "left point":                   R(Playback([(["MouseGrid"], 0.1), (["four", "four"], 0.1), (["click"], 0.0)]), rdescript="Mouse: Left Point"),
        "right point":                  R(Playback([(["MouseGrid"], 0.1), (["six", "six"], 0.1), (["click"], 0.0)]), rdescript="Mouse: Right Point"),
        "center point":                 R(Playback([(["MouseGrid"], 0.1), (["click"], 0.0)]), rdescript="Mouse: Center Point"),
        }
    extras = [
              Dictation("text"),
              Dictation("mim"),
              IntegerRefST("n", 1, 1000),
              
             ]
    defaults = {"n": 1, "mim":""}

#---------------------------------------------------------------------------

grammar = None

if not settings.WSR:
    grammar = Grammar("Dragon Naturallyspeaking")
    grammar.add_rule(CommandRule(name="dragon"))
    grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None