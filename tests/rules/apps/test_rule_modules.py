from tests.test_util.modules_testing import ModulesTestCase


class AppsModulesTestCase(ModulesTestCase):
    def _rule_modules(self):
        from castervoice.rules.apps.browser import firefox, chrome
        from castervoice.rules.apps.editor import jetbrains
        from castervoice.rules.apps.speech_engine.dragon_rules import dragon2
        from castervoice.rules.apps.speech_engine.dragon_rules import dragon
        from castervoice.rules.apps.editor.eclipse_rules import eclipse2
        from castervoice.rules.apps.editor.eclipse_rules import eclipse
        from castervoice.rules.apps.mouse_grids import gridlegion
        from castervoice.rules.apps.mouse_grids import griddouglas
        from castervoice.rules.apps.mouse_grids import gridrainbow
        from castervoice.rules.apps.file_manager.totalcmd_rules import totalcmd2
        from castervoice.rules.apps.file_manager.totalcmd_rules import totalcmd
        from castervoice.rules.apps.editor.vscode_rules import vscode
        from castervoice.rules.apps.editor.vscode_rules import vscode2
        from castervoice.rules.apps.file_manager import fman
        from castervoice.rules.apps.pdf import foxitreader
        from castervoice.rules.apps.pdf import adobe_acrobat
        from castervoice.rules.apps.microsoft_office import excel
        from castervoice.rules.apps.microsoft_office import outlook
        from castervoice.rules.apps.windows_os import winword
        from castervoice.rules.apps.terminal import gitbash
        from castervoice.rules.apps.windows_os import file_dialogue
        from castervoice.rules.apps.windows_os import explorer
        from castervoice.rules.apps.editor import visualstudio
        from castervoice.rules.apps.git_clients import kdiff3
        from castervoice.rules.apps.git_clients import githubdesktop
        from castervoice.rules.apps.speech_engine import wsr
        from castervoice.rules.apps.editor import lyx
        from castervoice.rules.apps.editor import notepadplusplus
        from castervoice.rules.apps.editor import sqldeveloper
        from castervoice.rules.apps.editor import ssms
        from castervoice.rules.apps.editor import rstudio
        from castervoice.rules.apps.editor import atom
        from castervoice.rules.apps.editor import flashdevelop
        from castervoice.rules.apps.editor import msvc
        from castervoice.rules.apps.editor import typora
        from castervoice.rules.apps.editor import sublime
        from castervoice.rules.apps.editor import emacs
        from castervoice.rules.apps.chat import gitter, MSTeamsRule, webexteams
        from castervoice.rules.apps.atlassian import jira
        return [chrome, firefox, jetbrains, adobe_acrobat, atom,
                dragon, dragon2, eclipse, eclipse2, emacs, excel,
                explorer, file_dialogue, flashdevelop, fman,
                foxitreader, gitbash, githubdesktop, gitter,
                griddouglas, gridlegion, gridrainbow, jira, kdiff3, lyx,
                msvc, MSTeamsRule, notepadplusplus, outlook, rstudio,
                sqldeveloper, ssms, sublime, totalcmd, totalcmd2,
                typora, visualstudio, vscode, vscode2, winword,
                webexteams, wsr]