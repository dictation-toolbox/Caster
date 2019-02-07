from dragonfly import (Grammar, Dictation, Repeat)

from castervoice.lib import control
from castervoice.lib import settings
from castervoice.lib.dfplus.additions import IntegerRefST
from castervoice.lib.dfplus.merge import gfilter
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R
from castervoice.lib.context import AppContext
from castervoice.lib.actions import Key


class TotalCommanderRule (MergeRule):
    pronunciation = "total commander"

    mapping = {
        "find [in] files":
            R(Key('a-f7'),
              rdescript="Total Commander: find"),
        "view":
            R(Key('f3'),
              rdescript="Total Commander: find next/view file"),
        "edit":
            R(Key('f4'),
              rdescript="Total Commander: edit file"),
        "copy":
            R(Key('f5'),
              rdescript="Total Commander: copy"),
        "move":
            R(Key('f6'),
              rdescript="Total Commander: move file"),
        "new directory":
            R(Key('f7'),
              rdescript="Total Commander: create directory"),
        "wipe":
            R(Key('s-delete'),
              rdescript="Total Commander: really delete file"),
        "FTP":
            R(Key('c-f'),
              rdescript="Total Commander: Connect to FTP"),
        "synchronize":
            R(Key('a-c') + Key('y'),
              rdescript="Total Commander: synchronize dirs"),
        "sort by name":
            R(Key('c-f3'),
              rdescript="Total Commander: sort files by name"),
        "sort by extension":
            R(Key('c-f4'),
              rdescript="Total Commander: sort files by extension"),
        "sort by date":
            R(Key('c-f5'),
              rdescript="Total Commander: sort files by date"),
        "sort by size":
            R(Key('c-f6'),
              rdescript="Total Commander: sort files by size"),
        "file filter":
            R(Key('c-f12'),
              rdescript="Total Commander: filter files"),
        "new tab":
            R(Key('c-t'),
              rdescript="Total Commander: new tab"),
        "multi rename":
            R(Key('c-m'),
              rdescript="Total Commander: batch rename files"),
        "display thumbnails":
            R(Key('cs-f1'),
              rdescript="Total Commander: display thumbnails in panel"),
        "display list":
            R(Key('c-f1'),
              rdescript="Total Commander: display plain file list in panel"),
        "display details":
            R(Key('c-f2'),
              rdescript="Total Commander: display details in panel"),
        "display file tree":
            R(Key('c-f8'),
              rdescript="Total Commander: display file tree in panel"),
    }

class SyncDirsRule (MergeRule):
    pronunciation = "total commander synchronize directories"

    mapping = {
        "compare files":
            R(Key('c-f3'),
              rdescript="Sync Dirs: compare right and left"),
        "copy left":
            R(Key('c-l'),
              rdescript="Sync Dirs: select for copying left"),
        "copy right":
            R(Key('c-r'),
              rdescript="Sync Dirs: select for copying right"),
        "view right":
            R(Key('s-f3'),
              rdescript="Sync Dirs: view right"),
        "remove selection":
            R(Key('c-m'),
              rdescript="Sync Dirs: remove selection"),
        "synchronize":
            R(Key('a-c'),
              rdescript="Total Commander: synchronize button"),
    }

context = AppContext(executable="totalcmd") | AppContext(executable="totalcmd64")
grammar = Grammar("Total Commander", context=context)
syncdir_context = AppContext(executable="totalcmd", title='Synchronize directories') 
syncdir_context |= AppContext(executable="totalcmd64", title='Synchronize directories')
syncdir_grammar = Grammar("Total Commander Sync Dirs", context=syncdir_context)

if settings.SETTINGS["apps"]["totalcmd"]:
    if settings.SETTINGS["miscellaneous"]["rdp_mode"]:
       control.nexus().merger.add_global_rule(SyncDirsRule())
       control.nexus().merger.add_global_rule(TotalCommanderRule())
    else:
        syncdir_rule = SyncDirsRule(name="totalcmd sync dirs")
        gfilter.run_on(syncdir_rule)
        syncdir_grammar.add_rule(syncdir_rule)
        syncdir_grammar.load()
        rule = TotalCommanderRule(name="totalcmd")
        gfilter.run_on(rule)
        grammar.add_rule(rule)
        grammar.load()
