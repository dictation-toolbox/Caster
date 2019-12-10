import re

def set_rdescript(mapping, rcn):
    for spec, action in mapping.items():
        # pylint: disable=no-member
        if hasattr(action, "rdescript") and action.rdescript is None:
            mapping[spec].rdescript = _create_rdescript(spec, rcn)

def _create_rdescript(spec, rcn):
    rule_name = rcn
    for unnecessary in ["Non", "Rule", "Ccr", "CCR"]:
        rule_name = rule_name.replace(unnecessary, "")
    extras = ""
    named_extras = re.findall(r"<(.*?)>", spec)
    if named_extras:
        extras = ", %(" + ")s, %(".join(named_extras) + ")s"
    return "%s: %s%s" % (rule_name, spec, extras)
