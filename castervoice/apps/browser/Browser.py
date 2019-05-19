#
# __author__ = "lexxish"
# __license__ = "LGPL"
# __version__ = "3.0"
#

from aenum import MultiValueEnum


class Browser(MultiValueEnum):
    GO_BACK = 1, "back"
    GO_FORWARD = 2, "forward"