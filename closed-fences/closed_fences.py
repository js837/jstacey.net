from fractions import Fraction

INTERSECT_AS_SUBSET, INTERSECT, NO_INTERSECT = range(3)
INF = float('Inf')


class Point(object):
    """
    Cartesian point class supporting rationals.
    """

    # We're immutable, so use __new__ (not __init__)
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
        if isinstance(scalar, (int, float, long, Fraction)):
            return Point(scalar * self.x, scalar * self.y)
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
        n = point - self.start
        d = self.end - self.start

        # First check if point is on infinite line
        if n.x * d.y == n.y * d.x:
            # Now check if it's on the segment
            if n.x == d.x or n.x // d.x == 0:
                return True
        return False

    def reverse(self):
        return Line(self.end, self.start)

    def get_side(self, point):
        """
        Output -1, 0, +1 depending on the side of the line
        that the point lies.
        """
        d = (self.start - self.end).y * (point - self.start).x + \
            (self.end - self.start).x * (point - self.start).y

        return cmp(d, 0)  # signum(d)

    @staticmethod
    def get_angle(l1, l2):
        # This isn't actually the line-angle but is equivalent for ordering
        # purposes.
        dot = Line.dot_prod(l1, l2)
        dot_sign = cmp(dot, 0)
        return dot_sign * Fraction(dot ** 2, Line.dot_prod(l1, l1)
                                   * Line.dot_prod(l2, l2))

    @staticmethod
    def intersect(l1, l2):
        """
        Given two lines - their intersection type.
        (INTERSECT_AS_SUBSET | INTERSECT | NO_INTERSECT)

        If intersection return the t, s values (fractional).
        """

        a = (l1.end - l1.start).x
        b = (l2.start - l2.end).x
        c = (l1.end - l1.start).y
        d = (l2.start - l2.end).y

        det = a * d - b * c
        if det == 0:
            if (l2.start in l1) or (l2.end in l1):
                # Subset
                return INTERSECT_AS_SUBSET, 0, 0
            else:
                # Parallel
                return NO_INTERSECT, 0, 0

        q = (l2.start - l1.start).x
        r = (l2.start - l1.start).y

        t = Fraction((d * q - b * r), det)
        s = Fraction((-c * q + a * r), det)

        return INTERSECT, t, s

    @staticmethod
    def dot_prod(l1, l2):
        """
        Dot product of line1 and line2
        """
        a = l1.end - l1.start
        b = l2.end - l2.start
        return a.x * b.x + a.y * b.y


def visible_sides(eye, point_list):
    """
    Given a point. Determine the fences that are (fully or partially)
    visible from here.
    """
    N = len(point_list)

    lines = [Line(point_list[i], point_list[(i + 1) % N]) for i in range(N)]
    visible_counts = [False for _ in range(N)]

    for point in point_list:
        eye_line = Line(eye, point)

        # Create two groups of lines: right/right of the eye-line
        # Lines which completely intersect the eye-line (0<t<1) are in
        # both groups.
        left = (INF, 0, -1)
        right = (INF, 0, -1)

        for line_i, line in enumerate(lines):

            intersect_type, t, s = Line.intersect(line, eye_line)

            if intersect_type == INTERSECT and s >= 0 and (0 <= t <= 1):

                # Case 1: Line completely intersects eye-line
                if 0 < t < 1:
                    # No angle required because fence does not intersect
                    left = min(left, (s, 0, line_i))
                    right = min(right, (s, 0, line_i))

                # Case 2: Eye-line touches a corner
                else:
                    # t == 0 or t==1
                    if t == 1:
                        line = line.reverse()

                    side = Line.get_side(eye_line, line.end)
                    line_angle = Line.get_angle(eye_line, line)

                    if side == +1:
                        left = min(left, (s, line_angle, line_i))
                    elif side == -1:
                        right = min(right, (s, line_angle, line_i))

        if left[0] != INF:
            visible_counts[left[2]] = True

        if right[0] != INF:
            visible_counts[right[2]] = True

    return visible_counts


def main():
    pass


if __name__ == '__main__':
    main()
