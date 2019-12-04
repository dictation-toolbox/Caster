from tests.test_util.modules_testing import ModulesTestCase


class CCRModulesTestCase(ModulesTestCase):
    def _rule_modules(self):
        from castervoice.ccr.bash import bash
        from castervoice.ccr.core import punctuation, numeric, nav2, nav, alphabet, text_manipulation
        from castervoice.ccr.cpp import cpp
        from castervoice.ccr.csharp import csharp
        from castervoice.ccr.dart import dart
        from castervoice.ccr.go import go
        from castervoice.ccr.haxe import haxe
        from castervoice.ccr.html import html_rule
        from castervoice.ccr.java import java2, java
        from castervoice.ccr.javascript import javascript
        from castervoice.ccr.latex import latex
        from castervoice.ccr.markdown import markdown
        from castervoice.ccr.matlab import matlab2, matlab
        from castervoice.ccr.prolog import prolog2, prolog
        from castervoice.ccr.python import python2, python
        from castervoice.ccr.r import r
        from castervoice.ccr.recording import history, bringme, again
        from castervoice.ccr.recording.alias import simple_alias, chain_alias
        from castervoice.ccr.rust import rust2, rust
        from castervoice.ccr.sql import sql
        from castervoice.ccr.vhdl import vhdl2, vhdl
        from castervoice.ccr.voice_dev_commands import voice_dev_commands
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
