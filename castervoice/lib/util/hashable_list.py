class HashableList(object):
    """
    A structure that stores a list of str()-able items,
    but can also be used as a key in a dict.

    This is not a very good general purpose data structure.
    It has a very specific use in DetailsCompatibilityChecker.
    """
    def __init__(self, delimiter=","):
        self._str_representation = ""
        self._list_representation = []
        self._delimiter = delimiter

    def add(self, item):
        self._str_representation += str(item) + self._delimiter
        self._list_representation.append(item)

    def get_string(self):
        return self._str_representation

    def get_list(self):
        return list(self._list_representation)

    def __len__(self):
        return len(self._list_representation)

    def __hash__(self):
        return hash(self._str_representation)

    def __eq__(self, other):
        return self.get_string() == other.get_string()
