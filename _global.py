from dragonfly import *
import os, natlink


class MainRule(MappingRule):
    mapping = {
    
	'deactivate': 			Playback([(["go", "to", "sleep"], 0.0)]),
	'scratch': 			Playback([(["scratch", "that"], 0.0)]),
    '(number|numbers) mode':             Playback([(["numbers", "mode", "on"], 0.0)]),
    'spell mode':             Playback([(["spell", "mode", "on"], 0.0)]),
    '(normal|dictation) mode':             Playback([(["dictation", "mode", "on"], 0.0)]),
	
    #mouse control
    'kick left': 			Mouse("left:1"),#Playback([(["mouse", "left", "click"], 0.0)]),something
	'kick mid': 				Mouse("middle:1"),#Playback([(["mouse", "middle", "click"], 0.0)]),
	'kick right': 			Mouse("right:1"),#Playback([(["mouse", "right", "click"], 0.0)]),
    '(kick double|double kick)':           Mouse("left:2"),
	'drag':				Mouse("left:down"),
	'release':			Mouse("left:up"),
    'right drag':                Mouse("right:down"),
    'right release':            Mouse("right:up"),
    
    
    #keyboard shortcuts
	'email one':			        Text("synkarius@gmail.com"),
	'email two':			        Text("dconway1985@gmail.com"),
    'save [work]':                  Key("c-s"),
    'enter':                        Key("enter"),
    "down <xtimes>":                Key("down") * Repeat(extra="xtimes"),
    "up <xtimes>":                  Key("up") * Repeat(extra="xtimes"),
    "end of line":                  Key("end"),
    "end of (all lines|text|page)": Key("c-end"),
    
    #program / function shortcuts
    #Open google chromewww.pandora.comopen goopen googleopen google chromewww.pandora.comto something
    # 
    
    '(open|launch) eclipse':        BringApp(r"D:\PROGRAMS\NON_install\eclipse\eclipse.exe"),
    '(open|launch) everything':        BringApp(r"D:\PROGRAMS\NON_install\Everything"),
    '(open|launch) chrome':        BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    '(open|launch) search':        BringApp(r"D:\PROGRAMS\NON_install\AstroGrep\AstroGrep.exe"),
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    
    #military alphabet
    "alpha": Key("a"),
    "bravo": Key("b"),
    "charlie": Key("c"),
    "delta": Key("d"),
    "echo": Key("e"),
    "foxtrot": Key("f"),
    "golf": Key("g"),
    "hotel": Key("h"),
    "India": Key("i"),
    "Juliet": Key("j"),
    "kilo": Key("k"),
    "Lima": Key("l"),
    "Mike": Key("m"),
    "November": Key("n"),
    "oscar": Key("o"),
    "papa": Key("p"),
    "Quebec": Key("q"),
    "Romeo": Key("r"),
    "Sierra": Key("s"),
    "tango": Key("t"),
    "uniform": Key("u"),
    "victor": Key("v"),
    "whiskey": Key("w"),
    "x-ray": Key("x"),
    "yankee": Key("y"),
    "Zulu": Key("z"),
    
    #'(put on|play) [some] music':   BringApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    #                                +WaitWindow("Chrome", "chrome.exe", 2000)+Key("f6,w,w,w,dot,p,a,n,d,o,r,a,dot,c,o,m,enter"),
    }
    extras = [
              IntegerRef("xtimes", 1, 100),
              Dictation("text"),
              Dictation("text2")
             ]
    defaults ={"xtimes": 1}

grammar = Grammar('Global')
grammar.add_rule(MainRule())
grammar.load()
#Reload Dragon