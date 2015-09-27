'''
Created on Sep 27, 2015

@author: synkarius
'''
from caster.lib import control
from caster.lib.dfplus.merge.ccrmerger import Inf


def scenario_1(mp):
    '''manually handle a conflicting spec'''
    if mp.type == Inf.APP:
        print "doing merge for apps"
        for spec in mp.rule1.mapping_actual().keys():
            if spec in mp.rule2.mapping_actual().keys():
                '''this filter function gives priority to
                app rules over global rules'''
                print "deleting conflicting spec", spec
                del mp.rule1.mapping_actual()[spec]

# control.nexus().merger.add_filter(scenario_1)