from castervoice.lib.merge.ccrmerging2.compatibility.base_compat_checker import BaseCompatibilityChecker
from castervoice.lib.merge.ccrmerging2.compatibility.compat_result import CompatibilityResult
from castervoice.lib.util.bidi_graph import BiDiGraph
from castervoice.lib.util.hashable_list import HashableList


class DetailCompatibilityChecker(BaseCompatibilityChecker):
    def compatibility_check(self, mergerules):
        """
        DetailCompatibilityChecker computes incompatibilities
        but eliminates nothing. This may be useful for certain
        kinds of advanced merge strategies.

        :param mergerules: collection of MergeRule
        :return: collection of CompatibilityResult
        """

        '''
        "RCN" = rule class name
        
        1. Invert the mapping. Rules are usually one to many with specs.
           Here, we want to get a mapping of spec to RCNs, where the 
           attached RCNs are all the rules which include that spec.
           This is O(n) for total specs processed.
        '''
        specs_to_lists_of_rcns = {}
        rcns_to_rules = {}
        for rule in mergerules:
            DetailCompatibilityChecker._invert_mapping(
                rule,
                rule.get_mapping().keys(),
                specs_to_lists_of_rcns)
            rcns_to_rules[rule.get_rule_class_name()] = rule

        '''
        2. Now we take the dict of spec to RCNs and discard the specs.
           Any list of RCNs larger than size 1 represents an incompatibility.
           However, the RCN lists need further grouping. At this point, they
           are grouped by spec. What we want is a graph, with each RCN
           pointing to its incompatible RCNs.
           
           Still O(n) for the total number of specs.
        '''
        previously_computed_groups = set()
        graph = BiDiGraph()
        # gomir = "group of mutually incompatible rules"
        for gomir in specs_to_lists_of_rcns.values():
            if len(gomir) == 1:
                continue

            if gomir.get_string() in previously_computed_groups:
                continue
            previously_computed_groups.add(gomir.get_string())

            graph.add(*gomir.get_list())

        '''
        3. Convert the incompatibility graph to a list of compat results.
        '''
        results = []
        for rcn in rcns_to_rules:
            rule = rcns_to_rules[rcn]
            incompats = graph.get_node(rcn)
            results.append(CompatibilityResult(rule, incompats))
        return results

    @staticmethod
    def _invert_mapping(rule, rule_specs, specs_to_rules):
        """
        Given a rule and its specs, associates each spec with its rule in
        'specs_to_rules'. This (A) groups incompatible rules together for
        further processing and (B) preserves which specs are responsible,
        in case we want a hook in here or something like that.

        Format is a space delimited string with a leading space
        """

        for spec in rule_specs:
            if spec not in specs_to_rules:
                specs_to_rules[spec] = HashableList()
            specs_to_rules[spec].add(rule.get_rule_class_name())
