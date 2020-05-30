from dragonfly import MappingRule, Function, Dictation, Choice
from castervoice.lib.merge.state.short import R
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.context import read_selected_without_altering_clipboard
from castervoice.asynch.corrections.manager import query_user_for_choice
from castervoice.rules.core.text_manipulation_rules import (
    text_manipulation_support as tm,
)
from castervoice.lib.merge.additions import IntegerRefST
import similar_sounding_words
from castervoice.lib import control


def correct_selected():
    """
    If there is any text selected, show the corrections window and
    allow the user to replace it.
    Returns False if there is no text selected.
    """
    selected_text = read_selected_without_altering_clipboard(True)
    if selected_text[0] == 2 or not selected_text[1]:
        return False
    else:
        selected_text = selected_text[1]
    query_user_for_choice(selected_text)
    return True


def correct_dictation(
    dictation, direction, number_of_lines_to_search, occurrence_number
):
    """
    Using the same search rules is the text manipulation commands,
    search for a matching word, and try to select it and show the corrections window.
    if the spoken word cannot be found, it will try to find any similar sounding words
    initial the corrections box for that instead.
    """
    application = tm.get_application()
    if direction == "up" or direction == "down":
        number_of_lines_to_search, direction = tm.deal_with_up_down_directions(direction, number_of_lines_to_search)
    text = tm.select_text_and_return_it(direction, number_of_lines_to_search, application)
    if not text:
        return 
    phrase = dictation.strip().lower()
    alternatives = [phrase] + similar_sounding_words.index.get(phrase, [])
    for phrase in alternatives:
        # TODO: Behaviour when there are multiple matches in the selected text
        # may not be expected
        positions = tm.get_start_end_position(text, phrase, direction, occurrence_number, "dictation")
        if not positions:
            continue
        left_index, right_index = positions
        tm.deal_with_inner_select(text, phrase, left_index, right_index, application)
        if correct_selected():
            break
    else:
        print("unable to find", alternatives)


class CorrectionsRule(MappingRule):
    """
    Rules for displaying the corrections window allowing a user to choose
    an alternate word or capitalization for the one that is selected.
    """

    mapping = {
        "fix (selected|selection)": R(
            Function(correct_selected), rdescript="Correct selected word"
        ),
        "fix [<direction>] [<number_of_lines_to_search>] [<occurrence_number>] <dictation>": R(
            Function(correct_dictation), rdescript="Correct dictated word",
        ),
    }

    extras = [
        Dictation("dictation"),
        IntegerRefST("number_of_lines_to_search", 1, 50),
        Choice(
            "occurrence_number",
            {
                "first": 1,
                "second": 2,
                "third": 3,
                "fourth": 4,
                "fifth": 5,
                "sixth": 6,
                "seventh": 7,
                "eighth": 8,
                "ninth": 9,
                "tenth": 10,
            },
        ),
        Choice(
            "direction",
            {"lease": "left", "ross": "right", "sauce": "up", "dunce": "down",},
        ),
    ]
    defaults = {
        "direction": "left",
        "number_of_lines_to_search": 0,
        "occurrence_number": 1,
    }


def get_rule():
    details = RuleDetails(name="text corrections")
    return CorrectionsRule, details
