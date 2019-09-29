from tests.test_util.modules_testing import ModulesTestCase


class CCRModulesTestCase(ModulesTestCase):
    def _rule_modules(self):
        from castervoice.lib.ccr.bash import bash
        from castervoice.lib.ccr.core import punctuation, numeric, nav2, nav, alphabet, text_manipulation
        from castervoice.lib.ccr.cpp import cpp
        from castervoice.lib.ccr.csharp import csharp
        from castervoice.lib.ccr.dart import dart
        from castervoice.lib.ccr.go import go
        from castervoice.lib.ccr.haxe import haxe
        from castervoice.lib.ccr.html import html_rule
        from castervoice.lib.ccr.java import java2, java
        from castervoice.lib.ccr.javascript import javascript
        from castervoice.lib.ccr.latex import latex
        from castervoice.lib.ccr.markdown import markdown
        from castervoice.lib.ccr.matlab import matlab2, matlab
        from castervoice.lib.ccr.prolog import prolog2, prolog
        from castervoice.lib.ccr.python import python2, python
        from castervoice.lib.ccr.r import r
        from castervoice.lib.ccr.recording import history, bringme, again
        from castervoice.lib.ccr.recording.alias import simple_alias, chain_alias
        from castervoice.lib.ccr.rust import rust2, rust
        from castervoice.lib.ccr.sql import sql
        from castervoice.lib.ccr.vhdl import vhdl2, vhdl
        from castervoice.lib.ccr.voice_dev_commands import voice_dev_commands
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
