"""Convert marks to letter grades and grade points."""

GRADE_BOUNDARIES = [
    (85, "A+", 4.0),
    (75, "A", 4.0),
    (70, "A-", 3.7),
    (65, "B+", 3.3),
    (60, "B", 3.0),
    (55, "B-", 2.7),
    (50, "C+", 2.3),
    (45, "C", 2.0),
    (40, "D", 1.0),
    (0, "F", 0.0),
]


def letter_grade(mark):
    """Return the letter grade for a mark out of 100."""
    return _lookup(mark)[1]


def grade_point(mark):
    """Return the grade point for a mark out of 100."""
    return _lookup(mark)[2]


def _lookup(mark):
    if not 0 <= mark <= 100:
        raise ValueError(f"mark must be between 0 and 100, got {mark}")
    for boundary in GRADE_BOUNDARIES:
        if mark >= boundary[0]:
            return boundary
    return GRADE_BOUNDARIES[-1]
