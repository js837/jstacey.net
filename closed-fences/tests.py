import unittest

from closed_fences import *

import svgwrite


class TestPointOnLine(unittest.TestCase):
    def test_mid(self):
        point = Point(1, 1)
        line = Line(Point(0, 0), Point(2, 2))
        self.assertIn(point, line)

    def test_mid_reverse(self):
        point = Point(1, 1)
        line = Line(Point(2, 2), Point(0, 0))
        self.assertIn(point, line)

    def test_startpoint(self):
        point = Point(2, 2)
        line = Line(Point(2, 2), Point(0, 0))
        self.assertIn(point, line)

    def test_endpoint(self):
        point = Point(0, 0)
        line = Line(Point(2, 2), Point(0, 0))
        self.assertIn(point, line)

    def test_not_on_line(self):
        point = Point(-100, 321)
        line = Line(Point(2, 2), Point(0, 0))
        self.assertNotIn(point, line)

    def test_not_on_extended_line(self):
        point = Point(3, 3)
        line = Line(Point(2, 2), Point(0, 0))
        self.assertNotIn(point, line)


class TestIntersectLines(unittest.TestCase):
    def test_simple(self):
        l1 = Line(Point(0, 0), Point(2, 2))
        l2 = Line(Point(0, 2), Point(2, 0))
        self.assertEqual(Line.intersect(l1, l2),
                         (INTERSECT, Fraction(1, 2), Fraction(1, 2)))

    def test_intersect_at_point(self):
        l1 = Line(Point(0, 0), Point(1, 1))
        l2 = Line(Point(1, 1), Point(2, 2))
        self.assertEqual(Line.intersect(l1, l2),
                         (INTERSECT_AS_SUBSET, 0, 0))

    def test_intersect_at_midpoint(self):
        l1 = Line(Point(0, 0), Point(2, 2))
        l2 = Line(Point(1, 1), Point(0, 2))
        self.assertEqual(Line.intersect(l1, l2),
                         (INTERSECT, Fraction(1, 2), 0))

    def test_subset(self):
        l1 = Line(Point(0, 0), Point(2, 2))
        l2 = Line(Point(1, 1), Point(3, 3))
        self.assertEqual(Line.intersect(l1, l2),
                         (INTERSECT_AS_SUBSET, 0, 0))

    def test_parallel1(self):
        l1 = Line(Point(0, 0), Point(1, 1))
        l2 = Line(Point(2, 2), Point(3, 3))
        self.assertEqual(Line.intersect(l1, l2),
                         (NO_INTERSECT, 0, 0))

    def test_parallel2(self):
        l1 = Line(Point(0, 0), Point(1, 1))
        l2 = Line(Point(1, 0), Point(2, 1))
        self.assertEqual(Line.intersect(l1, l2),
                         (NO_INTERSECT, 0, 0))

    def test_not_parallel_no_intersect(self):
        l1 = Line(Point(0, 0), Point(1, 1))
        l2 = Line(Point(5, 5), Point(-5, 5))
        intersection_type, t, s = Line.intersect(l1, l2)
        self.assertTrue(t>1)


class TestVisibleLines(unittest.TestCase):
    def _runner(self, eye_tuple, fence_list, expected, image_name, scale, box):
        eye = Point(*eye_tuple)
        fence = [Point(*fence_tuple) for fence_tuple in fence_list]
        visible = visible_sides(eye, fence)
        self.assertEqual(visible, expected)

        dwg = svgwrite.Drawing('images/{0}.svg'.format(image_name))

        dwg.viewbox(*box)

        n = len(fence)

        # Add the point
        dwg.add(dwg.circle((scale * eye.x, scale * eye.y), 10, fill='red'))

        # Add the shape
        for i in range(n):
            start, end = scale * fence[i], scale * fence[(i + 1) % n]
            if visible[i]:
                colour = svgwrite.rgb(100, 0, 0, '%')
            else:
                colour = svgwrite.rgb(0, 0, 0, '%')

            dwg.add(dwg.line((start.x, start.y), (end.x, end.y),
                             stroke=colour, stroke_width=5))

        dwg.save()

    def test_middle_of_square(self):
        eye = (1, 1)
        fence = [(0, 0), (2, 0), (2, 2), (0, 2)]
        scale, box = 200, (-5, -5, 410, 410)
        self._runner(eye, fence, [True, True, True, True], 'img01', scale, box)

    def test_simple_shape(self):
        eye = (1, -1)
        fence = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]
        scale, box = 200, (0, -210, 410, 615)
        self._runner(eye, fence, [True, False, False, False, False], 'img02',
                     scale, box)

    def test_simple_shape2(self):
        eye = (0, 1)
        fence = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]
        scale, box = 200, (-10, -5, 415, 410)
        self._runner(eye, fence, [False, False, False, True, True], 'img03',
                     scale, box)

    def test_simple_shape3(self):
        eye = (1, -1)
        fence = [(0, 0), (2, 0), (1, 2)]
        scale, box = 200, (0, -210, 410, 615)
        self._runner(eye, fence, [True, False, False], 'img04', scale, box)

    def test_points_left_and_right(self):
        eye = (6, 4)
        fence = [(0, 0), (10, 0), (10, 8), (0, 8), (0, 4), (2, 6), (4, 4),
                 (4, 6),
                 (8, 6), (8, 2), (4, 2), (2, 4), (0, 2)]
        scale, box = 200, (-5, -5, 2005, 1700)
        self._runner(eye, fence, [False, False, False, False, False, False, True,
                                  True, True, True, True, False, False]
                     , 'img05', scale, box)


if __name__ == '__main__':
    unittest.main()
