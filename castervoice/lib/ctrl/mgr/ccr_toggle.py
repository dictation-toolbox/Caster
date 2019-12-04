from castervoice.lib import settings


class CCRToggle(object):

    def is_active(self):
        return settings.SETTINGS["miscellaneous"]["ccr_on"]

    def set_active(self, active):
        settings.SETTINGS["miscellaneous"]["ccr_on"] = active
        settings.save_config()
