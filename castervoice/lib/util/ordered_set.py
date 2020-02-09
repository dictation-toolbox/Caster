class OrderedSet(object):

    def __init__(self, collection=[]):
        self._list = list(collection)
        self._set = set(collection)

    def add(self, item):
        if item not in self._set:
            self._list.append(item)
            self._set.add(item)

    def add_all(self, collection):
        [self.add(item) for item in collection]

    def remove(self, item):
        if item in self._set:
            self._list.remove(item)
            self._set.remove(item)

    def remove_all(self, collection):
        [self.remove(item) for item in collection]

    def update(self, item, add=True):
        """ Helps avoid ternaries. """
        if add:
            self.add(item)
        else:
            self.remove(item)

    def to_set(self):
        return set(self._set)

    def to_list(self):
        return list(self._list)
