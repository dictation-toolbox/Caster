#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Microsoft Outlook
Note: I believe Microsoft Outlook is by far the most Dragon friendly email application.
All text fields are full text control, and all of the menus should be say-what-you-see natively in Dragon.
So it should be possible to control Outlook for the most part without these commands but they will help.

"""
#---------------------------------------------------------------------------

from dragonfly import (Grammar, Dictation, Repeat, Function, Choice)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.actions import Key, Text
from castervoice.lib.context import AppContext
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R

def capitalize(text):
    output = str(text).title()
    Text(output).execute()

class OutlookRule(MergeRule):
    pronunciation = "Outlook"

    mapping = {

            "search [bar] [<dict>]": R(Key("c-e") + Text("%(dict)s"), rdescript="puts text in the search bar"),
                "(message list | messages)": R(Key("tab:3"), 
                    rdescript="moves the focus from the search bar to the messages list"),
            "empty search [bar]": R(Key("c-e, c-a, del"), rdescript="clear search bar"),
            "next pane [<n>]": R(Key("f6"), rdescript="go to next pane of Outlook") * Repeat(extra='n'),
            "(un|prior|previous) pane [<n>]": R(Key("s-f6"), rdescript="go to previous pane of Outlook") * Repeat(extra='n'),
            
            "[go] back": R(Key("a-left"), rdescript="go back"),
            "spell check": R(Key("f7"),  rdescript="spell check"),
            "refresh [mail]": R(Key("f9"), rdescript="refresh"),
            "find contact": R(Key("f11"), rdescript="find contact"),
            "address book": R(Key("cs-a"), rdescript="address book"),
            "save as": R(Key("f12"), rdescript="save as"), # only in mail view

            # create new thing
            "new (appointment | event)": R(Key("sc-a"), rdescript="new appointment"),
            "new contact": R(Key("cs-c"), rdescript="new contact"),
            "new folder": R(Key("cs-e"), rdescript="new folder"),
            "advanced (search| find)": R(Key("cs-f"), rdescript="advanced search"),
            "new office document": R(Key("cs-h"), rdescript="new office document"),
            "(inbox | go to inbox)": R(Key("cs-i"), rdescript="go to inbox"),
            "new journal entry": R(Key("cs-j"), rdescript="Outlook: new journal entry"),
            "new task": R(Key("cs-k"), rdescript="Outlook: new task"),
            "new contact group": R(Key("cs-l"), rdescript="Outlook: new contact group"),
            "(new message| new mail)": R(Key("cs-m"), rdescript="Outlook: compose new message"),
            "new note": R(Key("cs-n"), rdescript="Outlook: new note"),
            "open the new search folder window": R(Key("cs-p"), rdescript="open the new search folder window"),
            "new meeting request": R(Key("cs-q"), rdescript="Outlook: new meeting request"),
            "new task request": R(Key("cs-u"), rdescript="Outlook: new task request"),
            
            # new message window
            "to field": R(Key("a-dot"), rdescript="go to to field"),
            "c c field": R(Key("a-c"), rdescript="go to cc field"),
            "subject [field]": R(Key("a-u"), rdescript="go to subject field"),
            "subject <text>": R(Key("a-u") + Function(capitalize) + Key("tab"),
                rdescript="puts capitalized text in the subject field then moves to the body field"),
            "attach file": R(Key("n, a, f"), rdescript="attach file"),         
            "add to dictionary": R(Key("s-f10/2, a"), rdescript="add to dictionary"),
            "click send message": R(Key("a-s"), rdescript=""), # be careful
            "find and replace": R(Key("c-h"), rdescript="find and replace"),
            "check names": R(Key("c-k"), rdescript="check names against address book"),

            
            # folders pane
            "expand [that]": R(Key("asterisk"), rdescript="expand collapsible list"),
            "collapse [that]": R(Key("minus"), rdescript="collapse collapsible list"),

            # folders navigation
                # some of these may be user dependent, depends on the order of your folders
                    # which you can inspect by pressing control y
                # also I think some of these are built into Dragon 
            "[go to] sent mail": R(Key("c-y/10, s, enter"), rdescript="go to sent mail folder"),
            "go to drafts": R(Key("c-y/10, d, enter"), rdescript="go to drafts folder"),
            "go to trash": R(Key("c-y/10, t, enter"), rdescript="go to trash folder"),
            "go to spam": R(Key("c-y/10, s:2, enter"), rdescript="go to spam folder"),
            "go to starred": R(Key("c-y/10, s:3, enter"), rdescript="go to starred"),
            "go to important": R(Key("c-y/10, i:2, enter"), rdescript="go to important folder"),
            "go to outbox": R(Key("cs-o"), rdescript="go to outbox"),
            


            # center pane
            "sort by [<sort_by>]": R(Key("a-v/5, a, b/5, %(sort_by)s"),  rdescript="sort by blank, e.g. sort by date"),
            "reverse sort": R(Key("a-v, r, s"), rdescript="sort in reverse order"),
            "block sender": R(Key("a-h/3, j/3, b"), rdescript="block sender"),


            # reading pane
            "open attachment": R(Key("s-tab, enter"), rdescript="opens attachment if you haven't already pressed tab; otherwise you have to get the right amount of tabs"),
            "[open] attachment menu": R(Key("s-tab, right"), rdescript="opens attachment if you haven't already pressed tab; otherwise you have to get the right amount of tabs"),
            "next message [<n>]": R(Key("s-f6/10, down"), rdescript="goes to next message while in the reading pane") * Repeat(extra='n'),
            "(prior | previous) message [<n>]": R(Key("s-f6/20, up"), rdescript="goes to previous message while in the reading pane") * Repeat(extra='n'),
                

            "[select] next link": R(Key("tab"), rdescript="highlight next link"),
            "[select] (previous | prior) link": R(Key("s-tab"), rdescript="highlight previous link"),

            # calendar
            "workweek [view]": R(Key("ca-2"), rdescript="show work week view"),
            "full week [view]": R(Key("ca-3"), rdescript="show full week view"),
            "month view": R(Key("ca-4"), rdescript="show month view"),

            # message shortcuts
            "reply all": R(Key("cs-r"), rdescript="reply all"),
            "forward": R(Key("c-f"), rdescript="forward"),
            "Mark as read": R(Key("c-q"), rdescript="Mark as read"),
            "Mark as unread": R(Key("c-u"), rdescript="Mark as unread"),
            "reply": R(Key("c-r"), rdescript="reply"),
            "(folder | go to folder)": R(Key("c-y"), rdescript="go to folder list"),

            # navigation
            "mail view": R(Key("c-1"), rdescript="e-mail view"),
            "calendar": R(Key("c-2"), rdescript="calendar view"),
            "contacts": R(Key("c-3"), rdescript="contacts view"),
            "tasks": R(Key("c-4"), rdescript="tasks view"),
            "go to notes": R(Key("c-5"), rdescript="notes view"),
            "folder list": R(Key("c-6"), rdescript="go to folder list"),
            "next open message": R(Key("c-dot"),
                rdescript="goes to next message that you currently have open in a separate window"),
            "(prior | previous) open message": R(Key("c-comma"), 
                rdescript="goes to previous message that you currently have open in a separate window"),
            "previous view": R(Key("a-left"), rdescript="go to previous view in the main Outlook window"),
            "next view": R(Key("a-right"), rdescript="go to next view in the main Outlook window"),


    }
    extras = [
        Dictation("dict"),
        Dictation("text"),
        IntegerRefST("n", 1, 100),
        Choice("sort_by", {
                    "date": "d",
                    "from": "f",
                    "to": "t",
                    "size": "s",
                    "subject": "j",
                    "type": "t",
                    "attachments": "c",
                    "account": "o",
                }),
            
        
    ]
    defaults = {"n": 1, "dict": "", "text": "", "sort_by": ""}


#---------------------------------------------------------------------------

context = AppContext(executable="outlook")
grammar = Grammar("outlook", context=context)

if settings.SETTINGS["apps"]["outlook"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
        control.nexus().merger.add_global_rule(())
    else:
        rule = OutlookRule(name="outlook")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()



