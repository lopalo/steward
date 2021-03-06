import unittest
from steward import Component, Field, FieldComp, FieldDict, Error


class A(Component):
    a = Field()


class B(Component):
    a = FieldDict(A)


class TestDict(unittest.TestCase):
    def test_ctor(self):
        r = B()
        self.assertEqual(0, len(r.a))

    def test_from_plain(self):
        d = {'a': {1: {'a': 'a'},
                   2: {'a': 'b'},
                   3: {'a': 'c'}}}
        r = B.from_plain(d)
        self.assertEqual(3, len(r.a))
        self.assertIs(d, r.as_plain())
        self.assertIs(d['a'], r.a.as_plain())
        self.assertEqual('a', r.a[1].a)
        self.assertEqual('c', r.a[3].a)

    def test_setitem(self):
        d = {'a': {1: {'a': 'a'},
                   2: {'a': 'b'}}}
        r = B.from_plain(d)
        self.assertEqual(2, len(r.a))
        r.a[1] = A(a='d')
        self.assertEqual(2, len(r.a))
        self.assertEqual('d', r.a[1].a)
        self.assertEqual({'a': {1: {'a': 'd'},
                                2: {'a': 'b'}}}, r.as_plain())

    def test_add_item(self):
        r = B()
        r.a[1] = A(a='a')
        self.assertEqual(1, len(r.a))
        self.assertEqual({'a': {1: {'a': 'a'}}}, r.as_plain())
        self.assertIs(r.as_plain()['a'], r.a.as_plain())
        self.assertIs(r.as_plain()['a'][1], r.a.as_plain()[1])

    def test_delitem(self):
        d = {'a': {1: {'a': 'a'},
                   2: {'a': 'b'}}}
        r = B.from_plain(d)
        self.assertEqual(2, len(r.a))
        del r.a[1]
        self.assertEqual(1, len(r.a))
        self.assertEqual({'a': {2: {'a': 'b'}}}, r.as_plain())
