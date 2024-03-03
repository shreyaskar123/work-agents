import unittest
from slug_computation import compute_slug

class TestSlugComputation(unittest.TestCase):
    def test_compute_slug(self):
        self.assertEqual(compute_slug('abc'), list('abc') + list('defghijklmnopqrstuvwxyz'))
        self.assertEqual(compute_slug('cba'), list('abc') + list('defghijklmnopqrstuvwxyz'))
        self.assertEqual(compute_slug('abcxyz'), list('abcxyz') + list('defghijklmnopqrstuvw'))

if __name__ == '__main__':
    unittest.main()
