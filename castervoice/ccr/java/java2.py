from dragonfly import MappingRule, Paste

from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R


class JavaNon(MappingRule):
    mapping = {
        "try catch":
            R(Text("try{}catch(Exception e){}")),
        "deco override":
            R(Text("@Override")),
        "iterate and remove":
            R(Paste(
                "for (Iterator<TOKEN> iterator = TOKEN.iterator(); iterator.hasNext();) {\n\tString string = iterator.next();\nif (CONDITION) {\niterator.remove();\n}\n}"
            )),
        "string builder":
            R(Paste(
                "StringBuilder builder = new StringBuilder(); builder.append(orgStr); builder.deleteCharAt(orgStr.length()-1);"
            )),
    }


def get_rule():
    return JavaNon, RuleDetails(name="java companion")