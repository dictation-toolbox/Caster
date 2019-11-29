from tests.test_util.modules_testing import ModulesTestCase


class AppsModulesTestCase(ModulesTestCase):
    def _rule_modules(self):
        from castervoice.apps.browser import firefox, chrome
        from castervoice.apps.ide import jetbrains
        from castervoice.apps.dragon import dragon, dragon2
        from castervoice.apps.eclipse import eclipse, eclipse2
        from castervoice.apps.MouseGrids import griddouglas, gridrainbow, gridlegion
        from castervoice.apps.totalcmd import totalcmd, totalcmd2
        from castervoice.apps.vscode import vscode2, vscode
        from castervoice.apps import adobe_acrobat, atom, excel, emacs, explorer, \
            file_dialogue, gitbash, foxitreader, fman, flashdevelop, gitter, githubdesktop, lyx, kdiff3, \
            rstudio, outlook, notepadplusplus, msvc, sublime, ssms, sqldeveloper, \
            wsr, winword, visualstudio, typora
        return [chrome, firefox, jetbrains, adobe_acrobat, atom,
                dragon, dragon2, eclipse, eclipse2, emacs, excel,
                explorer, file_dialogue, flashdevelop, fman,
                foxitreader, gitbash, githubdesktop, gitter,
                griddouglas, gridlegion, gridrainbow, kdiff3, lyx,
                msvc, notepadplusplus, outlook, rstudio,
                sqldeveloper, ssms, sublime, totalcmd, totalcmd2,
                typora, visualstudio, vscode, vscode2, winword,
                wsr]