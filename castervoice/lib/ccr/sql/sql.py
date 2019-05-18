'''
Created on Sep 2, 2015

@author: synkarius
'''

from castervoice.lib import control
from castervoice.lib.actions import Key, Text
from castervoice.lib.dfplus.merge.mergerule import MergeRule
from castervoice.lib.dfplus.state.short import R


class SQL(MergeRule):
    pronunciation = "sequel"

    mapping = {
        "select":
            R(Text(" SELECT "), rdescript="SQL: Select"),
        "select (all | every)":
            R(Text(" SELECT * "), rdescript="SQL: Select All"),
        "from":
            R(Text(" FROM "), rdescript="SQL: From"),
        "where":
            R(Text(" WHERE "), rdescript="SQL: Where"),
        "between":
            R(Text(" BETWEEN "), rdescript="SQL: Between"),
        "lodge and ":
            R(Text(" AND "), rdescript="SQL: And"),
        "lodge or":
            R(Text(" OR "), rdescript="SQL: Or"),
        "it are in":
            R(Text(" IN "), rdescript="SQL: In"),
        "equals | equal to":
            R(Text(" = "), rdescript="SQL: Equals"),
        "not equals | not equal to":
            R(Text(" <> "), rdescript="SQL: Not Equal To"),
        "group by":
            R(Text(" GROUP BY "), rdescript="SQL: Group By"),
        "order by":
            R(Text(" ORDER BY "), rdescript="Order By"),
        "ascending":
            R(Text(" ASC "), rdescript="SQL: Ascending"),
        "descending":
            R(Text(" DESC "), rdescript="SQL: Descending"),
        "left join":
            R(Text(" LEFT JOIN "), rdescript="SQL: Left Join"),
        "inner join":
            R(Text(" INNER JOIN "), rdescript="SQL: Inner Join"),
        "right join":
            R(Text(" RIGHT JOIN "), rdescript="SQL: Right Join"),
        "full join":
            R(Text(" FULL JOIN "), rdescript="SQL: Full Join"),
        "join":
            R(Text(" JOIN "), rdescript="SQL: Join"),
        "on columns":
            R(Text(" ON "), rdescript="SQL: On"),
        "using":
            R(Text(" USING () ") + Key("left/5:2"), rdescript="SQL: Using"),
        "insert into":
            R(Text(" INSERT INTO "), rdescript="SQL: Insert"),
        "update":
            R(Text(" UPDATE TOKEN SET "), rdescript="SQL: Update"),
        "delete":
            R(Text(" DELETE "), rdescript="SQL: Delete"),
        "like":
            R(Text(" LIKE '%%'") + Key("left/5:2"), rdescript="SQL: Like"),
        "union":
            R(Text(" UNION "), rdescript="SQL: Union"),
        "alias as":
            R(Text(" AS "), rdescript="SQL: Alias As"),
        "is null":
            R(Text(" IS NULL "), rdescript="SQL: Is Null"),
        "is not null":
            R(Text(" IS NOT NULL "), rdescript="SQL: Is Not Null"),
        "fun max":
            R(Text(" MAX() ") + Key("left/5:2"), rdescript="SQL: Max"),
        "fun min":
            R(Text(" MIN() ") + Key("left/5:2"), rdescript="SQL: Min"),
        "fun count":
            R(Text(" COUNT() ") + Key("left/5:2"), rdescript="SQL: Count"),
        "fun average":
            R(Text(" AVG() ") + Key("left/5:2"), rdescript="SQL: Average"),
        "over partition by":
            R(Text(" OVER (PARTITION BY ) ") + Key("left/5:2"),
              rdescript="SQL: Over Partition By"),
    }

    extras = []
    defaults = {}


control.nexus().merger.add_global_rule(SQL())
