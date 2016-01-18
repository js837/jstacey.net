from fractions import Fraction
import operator

import math

INTERSECT_AS_SUBSET, INTERSECT, NO_INTERSECT = range(3)
INVALID_FENCE, VALID_FENCE = 'INVALIDFENCE', 'VALIDFENCE'
LEFT, RIGHT = 'LEFT', 'RIGHT'
INF = 10 ** 10


class Point(object):
    """
    Cartesian point class supporting rationals.
    """

    # We're immutable, so use __new__ not __init__
    def __new__(cls, x, y):
        self = super(Point, cls).__new__(cls)
        self.x, self.y = x, y
        return self

    def __repr__(self):
        return 'Point({0}, {1})'.format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        if isinstance(scalar, (int, Fraction)):
            return Point(scalar * self.x, scalar*self.y)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)


class Line(object):
    # We're immutable, so use __new__ not __init__
    def __new__(cls, start, end):
        self = super(Line, cls).__new__(cls)
        self.start, self.end = start, end
        return self

    def __repr__(self):
        return 'Line({0}, {1})'.format(repr(self.start), repr(self.end))

    def __contains__(self, point):
        nx = point.x - self.start.x
        dx = self.end.x - self.start.x
        ny = point.y - self.start.y
        dy = self.end.y - self.start.y

        # First check if point is on infinite line
        if nx * dy == ny * dx:
            # Now check if it's on the segment
            if nx == dx or nx // dx == 0:
                return True
        return False
#
#
# def point_on_line(point, line):
#     """
#     Check if a point is on a line.
#     """
#     line_s, line_e = line
#
#     a = point[0] - line_s[0]
#     b = line_e[1] - line_s[1]
#     c = point[1] - line_s[1]
#     d = line_e[0] - line_s[0]
#
#     # First check if lines are not parallel
#     if a * b == c * d:
#
#         # Lines are not parallel, need to decide if they cross
#         if a == d or a // d == 0:
#             return True
#
#     return False


def get_intersect_params(l1, l2):
    """
    :param line:
        l1, l2 are both lines of the form:
            ((l_s_x, l_s_y), (l_e_x, l_e_y))

    :return:
        Intersect_type, t, s
        Types:
            Intersect_type = [INTERSECT_AS_SUBSET, INTERSECT, NO_INTERSECT]
            t, s: Fraction
    """

    l1_s, l1_e = l1.start, l1.end
    l2_s, l2_e = l2.start, l2.end

    a = l1_e.x - l1_s.x
    b = -1 * (l2_e.x - l2_s.x)
    c = l1_e.y - l1_s.y
    d = -1 * (l2_e.y - l2_s.y)

    q = l2_s.x - l1_s.x
    r = l2_s.y - l1_s.y

    det = a * d - b * c
    if det == 0:
        if (l2_s in l1) or (l2_e in l1):
            # Subset
            return INTERSECT_AS_SUBSET, 0, 0
        else:
            # Parallel
            return NO_INTERSECT, 0, 0

    u = (d * q - b * r)
    v = (-c * q + a * r)

    t = Fraction(u, det)
    s = Fraction(v, det)

    return INTERSECT, t, s


def intersect(l1, l2):
    intersect_type, t, s = get_intersect_params(l1, l2)

    if intersect_type == INTERSECT_AS_SUBSET:
        return True

    elif intersect_type == NO_INTERSECT:
        return False

    elif intersect_type == INTERSECT:
        if 0 <= t <= 1 and 0 <= s <= 1:
            return True
    else:
        raise NotImplementedError


def is_valid_fence(coord_list):
    # """
    # Check if fence given by coord_list is a valid shape.
    #
    # >>> invalid_fence = [(0, 0), (2, 0), (2, 2), (1, -1),]
    # >>> is_valid_fence(invalid_fence) == VALID_FENCE
    # False
    #
    # >>> valid_fence = [(0, 0), (1, 0), (1, 1), (0, 1), (0,-1)]
    # >>> is_valid_fence(valid_fence) == VALID_FENCE
    # False
    #
    # >>> valid_fence = [(0, 0), (1, 0), (1, 1), (0, 1)]
    # >>> is_valid_fence(valid_fence) == VALID_FENCE
    # True
    # """

    N = len(coord_list)
    if N <= 3:
        return INVALID_FENCE

    lines = []

    # Deal with all segments except the last - i.e. we check for a valid
    # intersecting path in space.
    for i in range(N - 1):
        new_line = coord_list[i], coord_list[i + 1]

        # (1) Check coord_list[i + 1] is not on the last line we drew
        if lines and point_on_line(coord_list[i + 1], lines[-1]):
            return INVALID_FENCE

        # (2) Check for intersects in all other lines
        for line in lines[:-1]:
            if intersect(line, new_line):
                # Segment crosses another
                return INVALID_FENCE

        lines.append(new_line)

    # Deal with the final line segment separately.
    final_line = coord_list[0], coord_list[N - 1]

    # (1) Check that the first and last points are not on the final line
    if point_on_line(coord_list[1], final_line) or \
            point_on_line(coord_list[-2], final_line):
        return INVALID_FENCE
    # (2) Check the other N-2 lines for intersection
    for line in lines[1:-1]:
        if intersect(line, final_line):
            return INVALID_FENCE

    return VALID_FENCE



def get_length(line):
    """
    Get the Euclidean length of a line
    """
    t = line.start - line.end
    return math.sqrt(t.x**2 + t.y**2)


def get_side(point, line):
    """
    Given a point P(x, y)
    and a line L((x1, y1), (x2, y2))

    Output -1, 0, +1 depending on the side of the line
    that the point lies

    >>> get_side(Point(0, 1), Line(Point(0, 0), Point(1, 1))) \
        == get_side(Point(0, 2), Line(Point(0, 0), Point(1, 1)))
    True

    """
    line_s, line_e = line.start, line.end

    d = (line_s.y- line_e.y) * (point.x - line_s.x) + \
        (line_e.x - line_s.x) * (point.y - line_s.y)

    if d > 0:
        return +1
    elif d < 0:
        return -1
    else:
        return 0


def dot_prod(l1, l2):
    """
    Dot product of line1 and line2
    """
    a = l1.end - l1.start
    b = l2.end - l2.start
    return a.x * b.x + a.y * b.y


def get_angle(l1, l2):
    return float(dot_prod(l1, l2)) / (get_length(l1) * get_length(l2))


def visible_sides(eye, coord_list):
    """
    Given a point. Determine the fences that are (fully or partially)
    visible from here.
    """
    N = len(coord_list)
    point_list = [Point(*o) for o in coord_list]


    lines = [Line(point_list[i], point_list[(i + 1) % N]) for i in range(N)]
    visible_counts = [False for _ in range(N)]

    for point in point_list:
        eye_line = Line(Point(*eye), point)

        # Create two groups of lines: right/right of the eye-line
        # Lines which completely intersect the eye-line (0<t<1) are in
        # both groups.

        left = []
        right = []

        for line_i, line in enumerate(lines):

            intersect_type, t, s = get_intersect_params(line, eye_line)
            if intersect_type == INTERSECT and s >= 0:

                if 0 < t < 1:
                    line_angle = get_angle(eye_line, line)
                    left.append((line_i, s, line_angle))
                    right.append((line_i, s, line_angle))

                else:
                    if t == 0:
                        side = get_side(line.end, eye_line)
                        line_angle = get_angle(eye_line, Line(line.start, line.end))
                    elif t == 1:
                        side = get_side(line.start, eye_line)
                        line_angle = get_angle(eye_line, Line(line.end, line.start))

                    if side == +1:
                        left.append((line_i, s, line_angle))
                    elif side == -1:
                        right.append((line_i, s, line_angle))

        left.sort(key=lambda o: (o[1], o[2]))
        right.sort(key=lambda o: (o[1], o[2]))

        if left:
            line_i, s, line_angle = left[0]
            visible_counts[line_i] = True

        if right:
            line_i, s, line_angle = right[0]
            visible_counts[line_i] = True

    return visible_counts


def main():
    import doctest
    doctest.testmod()

    #Test a basic square:
    assert visible_sides((1,1), [(0,0),(2,0),(2,2),(0,2)]) ==\
    [True, True, True, True]

    #More complex
    assert visible_sides((0,-1), [(0,0),(2,0),(2,2),(0,2),(1,1)]) ==\
    [True, False, False, False, False]

    assert visible_sides((0, 1), [(0,0),(2,0),(2,2),(0,2),(1,1)]) ==\
    [False, False, False, True, True]

    assert visible_sides((1, -1), [(0,0),(2,0),(1,2)]) ==\
    [True, False, False]


if __name__ == '__main__':
    main()
