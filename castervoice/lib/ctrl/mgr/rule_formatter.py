import re

def _set_rdescripts(mapping, rcn):
    for spec, action in mapping.items():
        # pylint: disable=no-member
        _set_the_rdescript(action, spec, rcn)


def _set_the_rdescript(action, spec, rcn):
    if hasattr(action, "rdescript") and action.rdescript is None:
        action.rdescript = _create_rdescript(spec, rcn)

def _create_rdescript(spec, rcn):
    rule_name = rcn
    for unnecessary in ["Non", "Rule", "Ccr", "CCR"]:
        rule_name = rule_name.replace(unnecessary, "")
    extras = ""
    named_extras = re.findall(r"<(.*?)>", spec)
    if named_extras:
        extras = ", %(" + ")s, %(".join(named_extras) + ")s"
    return "%s: %s%s" % (rule_name, spec, extras)
