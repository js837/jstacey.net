from closed_fences import *
import unittest


class TestPointOnLine(unittest.TestCase):

    def test_mid(self):
        point = (1, 1)
        line = ((0, 0), (2, 2))
        self.assertEqual(point_on_line(point, line), True)

    def test_mid_reverse(self):
        point = (1, 1)
        line = ((2, 2), (0, 0))
        self.assertEqual(point_on_line(point, line), True)

    def test_startpoint(self):
        point = (2, 2)
        line = ((2, 2), (0, 0))
        self.assertEqual(point_on_line(point, line), True)

    def test_endpoint(self):
        point = (0, 0)
        line = ((2, 2), (0, 0))
        self.assertEqual(point_on_line(point, line), True)

    def test_not_on_line(self):
        point = (-100, 321)
        line = ((2, 2), (0, 0))
        self.assertEqual(point_on_line(point, line), False)

    def test_not_on_extended_line(self):
        point = (3, 3)
        line = ((2, 2), (0, 0))
        self.assertEqual(point_on_line(point, line), False)


if __name__ == '__main__':
    unittest.main()
