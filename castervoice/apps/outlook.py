#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#
"""
Command-module for Microsoft Outlook
Note (from Alex Boche 2019): In my opinion, Microsoft Outlook probably most Dragon-friendly email application.
All text fields are full text control, and all of the menus should be say-what-you-see natively in Dragon.
A good alternative to using Outlook is to use an e-mail website in Chrome or Firefox since these applications
support Wolfmanstout's accessibility API commands which can replace full text control.
Outlook users may want to consider purchasing Voice Computer which provides good numbering software
for the buttons and text fields in Outlook although a free and better alternative 
to Voice Computer may be coming soon.


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
    pronunciation = "outlook"

    mapping = {
    # create new thing
        "new (appointment | event)":
            R(Key("sc-a"), rdescript="Outlook: New Appointment"),
        "new contact":
            R(Key("cs-c"), rdescript="Outlook: New Contact"),
        "new folder":
            R(Key("cs-e"), rdescript="Outlook: New Folder"),
        "advanced (search| find)":
            R(Key("cs-f"), rdescript="Outlook: Advanced Search"),
        "new office document":
            R(Key("cs-h"), rdescript="Outlook: New Office Document"),
        "(inbox | go to inbox)":
            R(Key("cs-i"), rdescript="Outlook: Go to Inbox"),
        "new journal entry":
            R(Key("cs-j"), rdescript="Outlook: New Journal Entry"),
        "new task":
            R(Key("cs-k"), rdescript="Outlook: New Task"),
        "new contact group":
            R(Key("cs-l"), rdescript="Outlook: New Contact Group"),
        "(new message| new mail)":
            R(Key("cs-m"), rdescript="Outlook: Compose New Message"),
        "new note":
            R(Key("cs-n"), rdescript="Outlook: New Note"),
        "open the new search folder window":
            R(Key("cs-p"), rdescript="Outlook: Open the New Search Folder Window"),
        "new meeting request":
            R(Key("cs-q"), rdescript="Outlook: New Meeting Request"),
        "new task request":
            R(Key("cs-u"), rdescript="Outlook: New Task Request"),

    # new message window
        "to field":
            R(Key("a-dot"), rdescript="Outlook: Go to to Field"),
        "c c field":
            R(Key("a-c"), rdescript="Outlook: Go to Cc Field"),
        "subject [field]":
            R(Key("a-u"), rdescript="Outlook: Go to Subject Field"),
        "subject <text>":
            R(Key("a-u") + Function(capitalize) + Key("tab"),
              rdescript=
              "Outlook: Puts Capitalized Text in the Subject Field Then Moves to the Body Field"),
        "attach file":
            R(Key("n, a, f"), rdescript="Outlook: Attach File"),
        "add to dictionary":
            R(Key("s-f10/2, a"), rdescript="Outlook: Add to Dictionary"),
        "click send message":
            R(Key("a-s"), rdescript="Outlook: Click Send Message"),  # be careful
        "find and replace":
            R(Key("c-h"), rdescript="Outlook: Find And Replace"),
        "check names":
            R(Key("c-k"), rdescript="Outlook: Check Names Against Address Book"),
        "spell check":
            R(Key("f7"), rdescript="Outlook: Spell Check"),
        "save as":
            R(Key("f12"), rdescript="Outlook: Save As"),  # only in mail view

    # folders pane
        "expand [that]":
            R(Key("asterisk"), rdescript="Outlook: Expand Collapsible List"),
        "collapse [that]":
            R(Key("minus"), rdescript="Outlook: Collapse Collapsible List"),

    # folders navigation
        # some of these may be user dependent, depends on the order of your folders
        # which you can inspect by pressing control y
        # also I think some of these are built into Dragon
        "[go to] sent mail":
            R(Key("c-y/10, s, enter"), rdescript="Outlook: Go to Sent Mail Folder"),
        "go to drafts":
            R(Key("c-y/10, d, enter"), rdescript="Outlook: Go to Drafts Folder"),
        "go to trash":
            R(Key("c-y/10, t, enter"), rdescript="Outlook: Go to Trash Folder"),
        "go to spam":
            R(Key("c-y/10, s:2, enter"), rdescript="Outlook: Go to Spam Folder"),
        "go to starred":
            R(Key("c-y/10, s:3, enter"), rdescript="Outlook: Go to Starred"),
        "go to important":
            R(Key("c-y/10, i:2, enter"), rdescript="Outlook: Go to Important Folder"),
        "go to outbox":
            R(Key("cs-o"), rdescript="Outlook: Go to Outbox"),

    # center pane
        "sort by [<sort_by>]":
            R(Key("a-v/5, a, b/5, %(sort_by)s"),
              rdescript="Outlook: Sort By Blank, e.g. Sort By Date"),
        "reverse sort":
            R(Key("a-v, r, s"), rdescript="Outlook: Sort in Reverse Order"),
        "block sender":
            R(Key("a-h/3, j/3, b"), rdescript="Outlook: Block Sender"),
        "search [bar] [<dict>]":
            R(Key("c-e") + Text("%(dict)s"), rdescript="Outlook:Puts Text in the Search Bar"),
        "(message list | messages)":
            R(Key("tab:3"),
              rdescript="Outlook: Moves the Focus From the Search Bar to the Messages List"),
        "(empty | clear) search [bar]":
            R(Key("c-e, c-a, del/3, escape"), rdescript="Outlook: Clear Search Bar"),
            # from the search bar to get the focus into the messages is three tabs
            # pressing escape also seems to work.
        "refresh [mail]":
            R(Key("f9"), rdescript="Outlook: Refresh"),

    # reading pane
        "open attachment":
            R(Key("s-tab, enter"),
              rdescript=
              "Opens Attachment if You Haven't Already Pressed Tab; Otherwise You Have to Get the Right Amount Of Tabs"
              ),
        "[open] attachment menu":
            R(Key("s-tab, right"),
              rdescript=
              "Opens Attachment if You Haven't Already Pressed Tab; Otherwise You Have to Get the Right Amount Of Tabs"
              ),
        "next message [<n>]":
            R(Key("s-f6/10, down"),
              rdescript="Outlook: Goes to Next Message While in the Reading Pane")*
            Repeat(extra='n'),
        "(prior | previous) message [<n>]":
            R(Key("s-f6/20, up"),
              rdescript="Outlook: Goes to Previous Message While in the Reading Pane")*
            Repeat(extra='n'),
        "[select] next link":
            R(Key("tab"), rdescript="Outlook: Highlight Next Link"),
        "[select] (previous | prior) link":
            R(Key("s-tab"), rdescript="Outlook: Highlight Previous Link"),

    # calendar
        "workweek [view]":
            R(Key("ca-2"), rdescript="Outlook: Show Work Week View"),
        "full week [view]":
            R(Key("ca-3"), rdescript="OutloOk: Show Full Week View"),
        "month view":
            R(Key("ca-4"), rdescript="OutloOk: Show Month View"),

    # message shortcuts
        "reply [<dict>]":
            R(Key("c-r") + Text("%(dict)s"), rdescript="Outlook: Reply"),
        "reply all [<dict>]":
            R(Key("cs-r") + Text("%(dict)s"), rdescript="Outlook:Reply All"),
        "forward":
            R(Key("c-f"), rdescript="Outlook: Forward"),
        "Mark as read":
            R(Key("c-q"), rdescript="Outlook: Mark as Read"),
        "Mark as unread":
            R(Key("c-u"), rdescript="Outlook: Mark as Unread"),
        "(folder | go to folder)":
            R(Key("c-y"), rdescript="Outlook: Go to Folder List"),

    # navigation
        "next pane [<n>]":
            R(Key("f6"), rdescript="Outlook: Go to Next Pane of Outlook")*Repeat(extra='n'),
        "(un|prior|previous) pane [<n>]":
            R(Key("s-f6"), rdescript="Outlook: Go to Previous Pane of Outlook")*Repeat(extra='n'),
        "mail view":
            R(Key("c-1"), rdescript="Outlook: E-mail View"),
        "calendar":
            R(Key("c-2"), rdescript="Outlook: Calendar View"),
        "contacts":
            R(Key("c-3"), rdescript="Outlook: Contacts View"),
        "tasks":
            R(Key("c-4"), rdescript="Outlook: Tasks View"),
        "go to notes":
            R(Key("c-5"), rdescript="Outlook: Notes View"),
        "folder list":
            R(Key("c-6"), rdescript="Outlook: Go to Folder List"),
        "find contact":
            R(Key("f11"), rdescript="Outlook: Find Contact"),
        "address book":
            R(Key("cs-a"), rdescript="Outlook: Address Book"),
        "next open message":
            R(Key("c-dot"),
              rdescript=
              "Goes to Next Message That You Currently Have Open in a Separate Window"),
        "(prior | previous) open message":
            R(Key("c-comma"),
              rdescript=
              "Goes to Previous Message That You Currently Have Open in a Separate Window"
              ),
        "previous view":
            R(Key("a-left"), rdescript="Outlook: Go to Previous View in the Main Outlook window"),
        "next view":
            R(Key("a-right"), rdescript="Outlook: Go to Next View in the Main Outlook Window"),

    # misc
        "[go] back":
            R(Key("a-left"), rdescript="Outlook: Go Back"),
    }
    extras = [
        Dictation("dict"),
        Dictation("text"),
        IntegerRefST("n", 1, 100),
        Choice(
            "sort_by", {
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
        control.nexus().merger.add_global_rule(OutlookRule())
    else:
        rule = OutlookRule(name="outlook")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
