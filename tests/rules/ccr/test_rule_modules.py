from tests.test_util.modules_testing import ModulesTestCase


class CCRModulesTestCase(ModulesTestCase):
    def _rule_modules(self):
        from castervoice.rules.ccr.bash import bash
        from castervoice.rules.core import text_manipulation
        from castervoice.rules.core import numeric
        from castervoice.rules.core import nav
        from castervoice.rules.core import nav2
        from castervoice.rules.core import alphabet
        from castervoice.rules.core import punctuation
        from castervoice.rules.ccr.cpp import cpp
        from castervoice.rules.ccr.csharp import csharp
        from castervoice.rules.ccr.dart import dart
        from castervoice.rules.ccr.go import go
        from castervoice.rules.ccr.haxe import haxe
        from castervoice.rules.ccr.html import html_rule
        from castervoice.rules.ccr.java import java
        from castervoice.rules.ccr.java import java2
        from castervoice.rules.ccr.javascript import javascript
        from castervoice.rules.ccr.latex import latex
        from castervoice.rules.ccr.markdown import markdown
        from castervoice.rules.ccr.matlab import matlab
        from castervoice.rules.ccr.matlab import matlab2
        from castervoice.rules.ccr.prolog import prolog
        from castervoice.rules.ccr.prolog import prolog2
        from castervoice.rules.ccr.python import python2
        from castervoice.rules.ccr.python import python
        from castervoice.rules.ccr.r import r
        from castervoice.rules.ccr.recording import bringme
        from castervoice.rules.ccr.recording import history
        from castervoice.rules.ccr.recording import again
        from castervoice.rules.ccr.recording.alias import simple_alias
        from castervoice.rules.ccr.recording.alias import chain_alias
        from castervoice.rules.ccr.rust import rust
        from castervoice.rules.ccr.rust import rust2
        from castervoice.rules.ccr.sql import sql
        from castervoice.rules.ccr.vhdl import vhdl2
        from castervoice.rules.ccr.vhdl import vhdl
        from castervoice.rules.ccr.voice_dev_commands import voice_dev_commands
        return [bash, alphabet, nav, nav2, numeric, punctuation,
                text_manipulation, cpp, csharp, dart, go, haxe,
                html_rule, java, java2, javascript, latex,
                markdown, matlab, matlab2, prolog, prolog2,
                python, python2, r, chain_alias, simple_alias,
                again, bringme, history, rust, rust2, sql,
                vhdl, vhdl2, voice_dev_commands]

    def _run_rule_modifications_for_testing(self, rule_class):
        if rule_class.__name__ == "HistoryRule":
            rule_class._setup_recognition_history = lambda: None
