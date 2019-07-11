'''
THIS IS NO LONGER A USEFUL VALIDATION since rules can get reloaded.
'''


class PronunciationAvailableValidator(object):
    def _is_valid(self, rule, params):
        existing_pronunciations = params
        return not rule.get_pronunciation() in existing_pronunciations

    def _invalid_message(self):
        return "must have a unique pronunciation"
