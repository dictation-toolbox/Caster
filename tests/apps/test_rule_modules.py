from castervoice.apps import adobe_acrobat, atom, dragon2, dragon, eclipse, eclipse2, excel, emacs, explorer, \
    file_dialogue, gitbash, foxitreader, fman, flashdevelop, griddouglas, gitter, githubdesktop, lyx, kdiff3, \
    gridrainbow, gridlegion, rstudio, outlook, notepadplusplus, msvc, sublime, totalcmd, ssms, sqldeveloper, totalcmd2, \
    wsr, winword, vscode2, vscode, visualstudio, typora
from castervoice.apps.browser import firefox, chrome
from castervoice.apps.ide import jetbrains
from tests.test_util.modules_testing import ModulesTestCase


class AppsModulesTestCase(ModulesTestCase):
    def test_modules_get_rule_contents(self):
        modules_to_test = [chrome, firefox, jetbrains, adobe_acrobat, atom,
                           dragon, dragon2, eclipse, eclipse2, emacs, excel,
                           explorer, file_dialogue, flashdevelop, fman,
                           foxitreader, gitbash, githubdesktop, gitter,
                           griddouglas, gridlegion, gridrainbow, kdiff3, lyx,
                           msvc, notepadplusplus, outlook, rstudio,
                           sqldeveloper, ssms, sublime, totalcmd, totalcmd2,
                           typora, visualstudio, vscode, vscode2, winword,
                           wsr]
        self._test_modules_get_rule_contents(modules_to_test)