import unittest

from utils import ReversibleDict


class TestReversibleDict(unittest.TestCase):
    def setUp(self) -> None:
        self.d = ReversibleDict(a=1, b=2, c=3, d=2, e=1)

    def test_get(self) -> None:
        self.assertEqual(1, self.d['a'])
        self.assertEqual(3, self.d['c'])

    def test_inv_get(self) -> None:
        self.assertEqual({'a', 'e'}, self.d.inv[1])
        self.assertEqual({'c'}, self.d.inv[3])

    def test_set(self) -> None:
        self.d['a'] = 5
        self.assertEqual(5, self.d['a'])
        self.assertEqual({'a'}, self.d.inv[5])

    def test_inv_set(self) -> None:
        with self.assertRaises(TypeError):
            self.d.inv[1] = {'e'}
            print(self.d._inv)

    def test_clear(self):
        self.d.clear()
        self.assertEqual(0, len(self.d))
        self.assertEqual(0, len(self.d.inv))

    def test_update(self):
        self.d.update(dict(f=1, g=3))
        self.assertEqual({'a', 'e', 'f'}, self.d.inv[1])
        self.assertEqual({'c', 'g'}, self.d.inv[3])
        self.d.update(f=2, h=3)
        self.assertEqual({'a', 'e'}, self.d.inv[1])
        self.assertEqual({'b', 'd', 'f'}, self.d.inv[2])
        self.assertEqual({'c', 'g', 'h'}, self.d.inv[3])

    def test_setdefault(self):
        self.d.setdefault('a', 0)
        self.assertEqual(1, self.d['a'])
        self.assertEqual({'a', 'e'}, self.d.inv[1])
        self.d.setdefault('f', 0)
        self.assertEqual(0, self.d['f'])
        self.assertEqual({'f'}, self.d.inv[0])

    def test_pop(self):
        self.d.pop('a')
        self.assertRaises(KeyError, self.d.__getitem__, 'a')
        self.assertEqual({'e'}, self.d.inv[1])
        self.d.pop('e')
        self.assertRaises(KeyError, self.d.inv.__getitem__, 1)

    def test_popitem(self):
        self.d.popitem()
        self.assertRaises(KeyError, self.d.__getitem__, 'e')
        self.assertEqual({'a'}, self.d.inv[1])
        self.d.popitem()
        self.d.popitem()
        self.d.popitem()
        self.d.popitem()
        self.assertRaises(KeyError, self.d.inv.__getitem__, 1)
