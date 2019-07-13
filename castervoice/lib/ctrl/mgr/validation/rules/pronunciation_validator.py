'''
THIS IS NO LONGER A USEFUL VALIDATION since rules can get reloaded.
Since rules can get loaded in a second time, a pronunciation will not just come through once.
'''


class PronunciationAvailableValidator(object):

    def is_applicable(self, declared_ccrtype):
        return False

    def _is_valid(self, rule):
        return True

    def _invalid_message(self):
        return "must have a unique pronunciation"
