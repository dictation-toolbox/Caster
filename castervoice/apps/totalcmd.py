from castervoice.lib.imports import *

class TotalCommanderRule(MergeRule):
    pronunciation = "total commander"

    mapping = {
        "find [in] files":
            R(Key('a-f7'),
              rdescript="Total Commander: Find"),
        "view":
            R(Key('f3'),
              rdescript="Total Commander: Find Next/View File"),
        "edit":
            R(Key('f4'),
              rdescript="Total Commander: Edit File"),
        "copy":
            R(Key('f5'),
              rdescript="Total Commander: Copy"),
        "move":
            R(Key('f6'),
              rdescript="Total Commander: Move File"),
        "new directory":
            R(Key('f7'),
              rdescript="Total Commander: Create Directory"),
        "wipe":
            R(Key('s-delete'),
              rdescript="Total Commander: Really Delete File"),
        "FTP":
            R(Key('c-f'),
              rdescript="Total Commander: Connect to FTP"),
        "synchronize":
            R(Key('a-c') + Key('y'),
              rdescript="Total Commander: Synchronize Dirs"),
        "sort by name":
            R(Key('c-f3'),
              rdescript="Total Commander: Sort Files by Name"),
        "sort by extension":
            R(Key('c-f4'),
              rdescript="Total Commander: Sort Files by Extension"),
        "sort by date":
            R(Key('c-f5'),
              rdescript="Total Commander: Sort Files by Date"),
        "sort by size":
            R(Key('c-f6'),
              rdescript="Total Commander: Sort Files by Size"),
        "file filter":
            R(Key('c-f12'),
              rdescript="Total Commander: Filter Files"),
        "new tab":
            R(Key('c-t'),
              rdescript="Total Commander: New Tab"),
        "multi rename":
            R(Key('c-m'),
              rdescript="Total Commander: Batch Rename Files"),
        "display thumbnails":
            R(Key('cs-f1'),
              rdescript="Total Commander: Display Thumbnails in Panel"),
        "display list":
            R(Key('c-f1'),
              rdescript="Total Commander: Display Plain File List in Panel"),
        "display details":
            R(Key('c-f2'),
              rdescript="Total Commander: Display Details in Panel"),
        "display file tree":
            R(Key('c-f8'),
              rdescript="Total Commander: Display File Tree in Panel"),
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
control.non_ccr_app_rule(TotalCommanderRule(), context=context)

syncdir_context = context & AppContext(title='Synchronize directories')
control.non_ccr_app_rule(SyncDirsRule(), context=syncdir_context)
