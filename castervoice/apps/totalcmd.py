from castervoice.lib.imports import *


class TotalCommanderRule(MergeRule):
    pronunciation = "total commander"

    mapping = {
        "find [in] files": R(Key('a-f7')),
        "view": R(Key('f3')),
        "edit": R(Key('f4')),
        "copy": R(Key('f5')),
        "move": R(Key('f6')),
        "new directory": R(Key('f7')),
        "wipe": R(Key('s-delete')),
        "FTP": R(Key('c-f')),
        "synchronize": R(Key('a-c, y')),
        "sort by name": R(Key('c-f3')),
        "sort by extension": R(Key('c-f4')),
        "sort by date": R(Key('c-f5')),
        "sort by size": R(Key('c-f6')),
        "file filter": R(Key('c-f12')),
        "new tab": R(Key('c-t')),
        "multi rename": R(Key('c-m')),
        "display thumbnails": R(Key('cs-f1')),
        "display list": R(Key('c-f1')),
        "display details": R(Key('c-f2')),
        "display file tree": R(Key('c-f8')),
    }


class SyncDirsRule(MergeRule):
    pronunciation = "total commander synchronize directories"

    mapping = {
        "compare files": R(Key('c-f3')),
        "copy left": R(Key('c-l')),
        "copy right": R(Key('c-r')),
        "view right": R(Key('s-f3')),
        "remove selection": R(Key('c-m')),
        "synchronize": R(Key('a-c')),
    }


context = AppContext(executable="totalcmd") | AppContext(executable="totalcmd64")
control.non_ccr_app_rule(TotalCommanderRule(), context=context)

syncdir_context = context & AppContext(title='Synchronize directories')
control.non_ccr_app_rule(SyncDirsRule(), context=syncdir_context)
