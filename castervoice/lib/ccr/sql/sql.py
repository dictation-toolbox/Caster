from castervoice.lib.actions import Text, Key
from castervoice.lib.const import CCRType
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class SQL(MergeRule):
    pronunciation = "sequel"

    mapping = {
        "select":
            R(Text(" SELECT ")),
        "select (all | every)":
            R(Text(" SELECT * ")),
        "from":
            R(Text(" FROM ")),
        "where":
            R(Text(" WHERE ")),
        "between":
            R(Text(" BETWEEN ")),
        "lodge and ":
            R(Text(" AND ")),
        "lodge or":
            R(Text(" OR ")),
        "it are in":
            R(Text(" IN ")),
        "equals | equal to":
            R(Text(" = ")),
        "not equals | not equal to":
            R(Text(" <> ")),
        "group by":
            R(Text(" GROUP BY ")),
        "order by":
            R(Text(" ORDER BY ")),
        "ascending":
            R(Text(" ASC ")),
        "descending":
            R(Text(" DESC ")),
        "left join":
            R(Text(" LEFT JOIN ")),
        "inner join":
            R(Text(" INNER JOIN ")),
        "right join":
            R(Text(" RIGHT JOIN ")),
        "full join":
            R(Text(" FULL JOIN ")),
        "join":
            R(Text(" JOIN ")),
        "on columns":
            R(Text(" ON ")),
        "using":
            R(Text(" USING () ") + Key("left/5:2")),
        "insert into":
            R(Text(" INSERT INTO ")),
        "update":
            R(Text(" UPDATE TOKEN SET ")),
        "delete":
            R(Text(" DELETE ")),
        "like":
            R(Text(" LIKE '%%'") + Key("left/5:2")),
        "union":
            R(Text(" UNION ")),
        "alias as":
            R(Text(" AS ")),
        "is null":
            R(Text(" IS NULL ")),
        "is not null":
            R(Text(" IS NOT NULL ")),
        "fun max":
            R(Text(" MAX() ") + Key("left/5:2")),
        "fun min":
            R(Text(" MIN() ") + Key("left/5:2")),
        "fun count":
            R(Text(" COUNT() ") + Key("left/5:2")),
        "fun average":
            R(Text(" AVG() ") + Key("left/5:2")),
        "over partition by":
            R(Text(" OVER (PARTITION BY ) ") + Key("left/5:2")),
    }

    extras = []
    defaults = {}


def get_rule():
    return SQL, RuleDetails(ccrtype=CCRType.GLOBAL)
