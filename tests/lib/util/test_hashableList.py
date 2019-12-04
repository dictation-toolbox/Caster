from unittest import TestCase

from castervoice.lib.util.hashable_list import HashableList


class TestHashableList(TestCase):
    def test_get_string(self):
        hl = HashableList()
        hl.add("a")
        hl.add("b")
        hl.add("c")
        self.assertEqual("a,b,c,", hl.get_string())

    def test_get_list(self):
        hl = HashableList()
        hl.add("a")
        hl.add("b")
        hl.add("c")
        self.assertSequenceEqual(["a", "b", "c"], hl.get_list())

    def test_len(self):
        hl = HashableList()
        hl.add("ab")
        hl.add("bc")
        hl.add("cd")
        self.assertEqual(3, len(hl))

    def test_hash(self):
        d = {}
        key1 = HashableList()
        key1.add("abc")
        key1.add("xyz")
        d[key1] = 43
        key2 = HashableList()
        key2.add("abc")
        key2.add("xyz")
        self.assertEqual(43, d[key2])

    def test_eq(self):
        hl1 = HashableList()
        hl1.add("abc")
        hl1.add("xyz")
        hl2 = HashableList()
        hl2.add("abc")
        hl2.add("xyz")
        self.assertEqual(hl1, hl2)
        hl1.add(1)
        self.assertNotEqual(hl1, hl2)
