from fractions import Fraction
import operator

import math

INTERSECT_AS_SUBSET, INTERSECT, NO_INTERSECT = range(3)
INVALID_FENCE, VALID_FENCE = 'INVALIDFENCE', 'VALIDFENCE'
LEFT, RIGHT = 'LEFT', 'RIGHT'
INF = 10 ** 10


class Point(tuple):
    def __new__(self, x, y):
        return tuple.__new__(self, (x, y))

    def __add__(self, other):
        return Point(self[0] + other[0], self[1] + other[1])


def point_on_line(point, line):
    """
    Check if a point is on a line.
    """
    line_s, line_e = line

    a = point[0] - line_s[0]
    b = line_e[1] - line_s[1]
    c = point[1] - line_s[1]
    d = line_e[0] - line_s[0]

    # First check if lines are not parallel
    if a * b == c * d:

        # Lines are not parallel, need to decide if they cross
        if a == d or a // d == 0:
            return True

    return False


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

    l1_s, l1_e = l1
    l2_s, l2_e = l2

    a = l1_e[0] - l1_s[0]
    b = -(l2_e[0] - l2_s[0])
    c = l1_e[1] - l1_s[1]
    d = -(l2_e[1] - l2_s[1])

    q = l2_s[0] - l1_s[0]
    r = l2_s[1] - l1_s[1]

    det = a * d - b * c
    if det == 0:
        if point_on_line(l2_s, l1) or point_on_line(l2_e, l1):
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
    """
    Check if fence given by coord_list is a valid shape.

    >>> invalid_fence = [(0, 0), (2, 0), (2, 2), (1, -1),]
    >>> is_valid_fence(invalid_fence) == VALID_FENCE
    False

    >>> valid_fence = [(0, 0), (1, 0), (1, 1), (0, 1), (0,-1)]
    >>> is_valid_fence(valid_fence) == VALID_FENCE
    False

    >>> valid_fence = [(0, 0), (1, 0), (1, 1), (0, 1)]
    >>> is_valid_fence(valid_fence) == VALID_FENCE
    True
    """

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
    start, end = line
    d2 = (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
    return math.sqrt(d2)


def get_side(point, line):
    """
    Given a point P(x, y)
    and a line L((x1, y1), (x2, y2))

    Output -1, 0, +1 depending on the side of the line
    that the point lies

    >>> get_side((0, 1), ((0, 0), (1, 1))) == get_side((0, 2), ((0, 0), (1, 1)))
    True

    """
    line_s, line_e = line

    d = (line_s[1] - line_e[1]) * (point[0] - line_s[0]) + \
        (line_e[0] - line_s[0]) * (point[1] - line_s[1])

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
    l1_s, l1_e = l1
    l2_s, l2_e = l2

    A = (l1_e[0] - l1_s[0], l1_e[1] - l1_s[1])
    B = (l2_e[0] - l2_s[0], l2_e[1] - l2_s[1])

    return A[0] * B[0] + A[1] * B[1]


def get_angle(l1, l2):
    return float(dot_prod(l1, l2)) / (get_length(l1) * get_length(l2))


def visible_sides(point, coord_list):
    """
    Given a point. Determine the fences that are (fully or partially)
    visible from here.

    Test a basic square:
    >>> visible_sides((1,1), [(0,0),(2,0),(2,2),(0,2)])
    [True, True, True, True]

    More complex
    >>> visible_sides((0,-1), [(0,0),(2,0),(2,2),(0,2),(1,1)])
    [True, False, False, False, False]

    >>> visible_sides((0, 1), [(0,0),(2,0),(2,2),(0,2),(1,1)])
    [False, False, False, True, True]

    >>> visible_sides((1, -1), [(0,0),(2,0),(1,2)])
    [True, False, False]

    """
    N = len(coord_list)

    lines = [(coord_list[i], coord_list[(i + 1) % N]) for i in range(N)]
    visible_counts = [False for _ in range(N)]

    for coord in coord_list:
        eye_line = point, coord

        # Create two groups of lines: right/right of the eye-line
        # Lines which completely intersect the eye-line (0<t<1) are in
        # both groups.

        left = []
        right = []

        for line_i, line in enumerate(lines):
            line_s, line_e = line

            intersect_type, t, s = get_intersect_params(line, eye_line)
            if intersect_type == INTERSECT and s >= 0:

                if 0 < t < 1:
                    line_angle = get_angle(eye_line, line)
                    left.append((line_i, s, line_angle))
                    right.append((line_i, s, line_angle))

                else:
                    if t == 0:
                        side = get_side(line_e, eye_line)
                        line_angle = get_angle(eye_line, (line_s, line_e))
                    elif t == 1:
                        side = get_side(line_s, eye_line)
                        line_angle = get_angle(eye_line, (line_e, line_s))

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


if __name__ == '__main__':
    main()
