'''
Created on Sep 2, 2015

@author: synkarius
'''
from dragonfly.actions.action_key import Key
from dragonfly.actions.action_text import Text

from caster.lib import control
from caster.lib.dfplus.merge.mergerule import MergeRule
from caster.lib.dfplus.state.short import R


class SQL(MergeRule):
    pronunciation = "sequel"
    
    mapping = { 
        "select":                   R(Text(" select "), rdescript="SQL: Select"), 
        "select all":               R(Text(" select * "), rdescript="SQL: Select All"),
        "from":                     R(Text(" from "), rdescript="SQL: From"),
        "where":                    R(Text(" where "), rdescript="SQL: Where"),
        
        "lodge and ":               R(Text(" and "), rdescript="SQL: And"),
        "lodge or":                 R(Text(" or "), rdescript="SQL: Or"),
        "it are in":                R(Text(" in "), rdescript="SQL: In"),
        "equals | equal to":        R(Text(" = "), rdescript="SQL: Equals"),
        "not equals | not equal to":R(Text(" <> "), rdescript="SQL: Not Equal To"),
        
        
        
        
        "group by":                 R(Text(" group by "), rdescript="SQL: Group By"),
        "order by":                 R(Text(" order by "), rdescript="Order By"),
        "ascending":                R(Text(" asc "), rdescript="SQL: Ascending"),
        "descending":               R(Text(" desc "), rdescript="SQL: Descending"),
        
        "left join":                R(Text(" left join "), rdescript="SQL: Left Join"),
        "join":                     R(Text(" join "), rdescript="SQL: Join"),
        "on columns":               R(Text(" on "), rdescript="SQL: On"),
        "using":                    R(Text(" using () ")+Key("left/5:2"), rdescript="SQL: Using"),
        
        "insert into":              R(Text(" insert into "), rdescript="SQL: Insert"),
        "update":                   R(Text(" update NAME set "), rdescript="SQL: Update"),
        "delete":                   R(Text(" delete "), rdescript="SQL: Delete"),
        
        
        "like":                     R(Text(" like '%%'")+Key("left/5:2"), rdescript="SQL: Like"),
        
        "union":                    R(Text(" union "), rdescript="SQL: Union"),
        "alias as":                 R(Text(" as "), rdescript="SQL: Alias As"),  
        
        
        "is null":                  R(Text(" is null "), rdescript="SQL: Is Null"),
        "is not null":              R(Text(" is not null "), rdescript="SQL: Is Not Null"),
        
        "fun max":                  R(Text(" max() ")+Key("left/5:2"), rdescript="SQL: Max"),
        "fun count":                R(Text(" count() ")+Key("left/5:2"), rdescript="SQL: Count"),
        
        "over partition by":        R(Text(" over (partition by ) ")+Key("left/5:2"), 
                                      rdescript="SQL: Over Partition By"),
            
        }

    extras   = []
    defaults = {}

control.nexus().merger.add_global_rule(SQL())