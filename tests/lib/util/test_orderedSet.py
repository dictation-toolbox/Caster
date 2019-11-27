from unittest import TestCase

from castervoice.lib.util.ordered_set import OrderedSet


class TestOrderedSet(TestCase):
    def test_add(self):
        o = OrderedSet([])
        o.add(1)
        self._list_and_set_equal([1], o)

    def test_add_all(self):
        o = OrderedSet([1])
        o.add_all([2, 3])
        self._list_and_set_equal([1, 2, 3], o)

    def test_remove(self):
        o = OrderedSet([1, 2])
        o.remove(1)
        self._list_and_set_equal([2], o)

    def test_remove_all(self):
        o = OrderedSet([1, 2, 3])
        o.remove_all([1, 3])
        self._list_and_set_equal([2], o)

    def test_update(self):
        o = OrderedSet([])
        o.update(1, True)
        o.update(1, False)
        self._list_and_set_equal([], o)

    def _list_and_set_equal(self, expected_list, actual_ordered_set):
        self.assertEqual(actual_ordered_set.to_list(), expected_list)
        self.assertEqual(actual_ordered_set.to_set(), set(expected_list))
