from tests.test_util.modules_testing import ModulesTestCase

class CCRModulesTestCase(ModulesTestCase):
    def _rule_modules(self):
        from castervoice.rules.ccr.bash_rules import bash
        from castervoice.rules.ccr.cpp_rules import cpp
        from castervoice.rules.ccr.csharp_rules import csharp
        from castervoice.rules.ccr.dart_rules import dart
        from castervoice.rules.ccr.go_rules import go
        from castervoice.rules.ccr.haxe_rules import haxe
        from castervoice.rules.ccr.html_rules import html_rule
        from castervoice.rules.ccr.java_rules import java
        from castervoice.rules.ccr.java_rules import java2
        from castervoice.rules.ccr.javascript_rules import javascript
        from castervoice.rules.ccr.latex_rules import latex
        from castervoice.rules.ccr.markdown_rules import markdown
        from castervoice.rules.ccr.matlab_rules import matlab
        from castervoice.rules.ccr.matlab_rules import matlab2
        from castervoice.rules.ccr.prolog_rules import prolog
        from castervoice.rules.ccr.prolog_rules import prolog2
        from castervoice.rules.ccr.python_rules import python2
        from castervoice.rules.ccr.python_rules import python
        from castervoice.rules.ccr.r_rules import r
        from castervoice.rules.ccr.recording_rules import bringme
        from castervoice.rules.ccr.recording_rules import history
        from castervoice.rules.ccr.recording_rules import again
        from castervoice.rules.ccr.recording_rules.alias import simple_alias
        from castervoice.rules.ccr.recording_rules.alias import chain_alias
        from castervoice.rules.ccr.rust_rules import rust
        from castervoice.rules.ccr.rust_rules import rust2
        from castervoice.rules.ccr.sql_rules import sql
        from castervoice.rules.ccr.vhdl_rules import vhdl2
        from castervoice.rules.ccr.vhdl_rules import vhdl
        from castervoice.rules.ccr.voice_dev_commands_rules import voice_dev_commands
        return [bash, cpp, csharp, dart, go, haxe,
                html_rule, java, java2, javascript, latex,
                markdown, matlab, matlab2, prolog, prolog2,
                python, python2, r, chain_alias, simple_alias,
                again, bringme, history, rust, rust2, sql,
                vhdl, vhdl2, voice_dev_commands]

    def _run_rule_modifications_for_testing(self, rule_class):
        if rule_class.__name__ == "HistoryRule":
            rule_class._setup_recognition_history = lambda: None
