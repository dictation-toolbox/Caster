'''
Created on May 5 2019

@author: kendonb
'''
from dragonfly import Function, MappingRule

from castervoice.lib import control, automation

_NEXUS = control.nexus()


class DevHelperNon(MappingRule):
    mapping = {
        "checkout [this] pull request [locally]":
            R(Function(automation.github_branch_pull_request),
                rdescript="Github: Checkout pull request locally"),

    }

control.nexus().merger.add_global_rule(DevHelperNon())
