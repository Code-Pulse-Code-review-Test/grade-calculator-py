"""Tests for grading and GPA."""

import unittest

from grades.gpa import (
    ModuleResult,
    best_module,
    calculate_gpa,
    class_for_gpa,
    failed_modules,
    weighted_average,
)
from grades.grading import grade_point, letter_grade


class GradingTest(unittest.TestCase):
    """Letter grades and grade points."""

    def test_boundaries(self):
        """Marks on a boundary get the higher grade."""
        self.assertEqual(letter_grade(85), "A+")
        self.assertEqual(letter_grade(74.9), "A-")
        self.assertEqual(letter_grade(40), "D")
        self.assertEqual(letter_grade(39), "F")

    def test_out_of_range(self):
        """Marks outside 0-100 are rejected."""
        with self.assertRaises(ValueError):
            grade_point(101)


class GpaTest(unittest.TestCase):
    """GPA and degree class."""

    def test_weighted_gpa(self):
        """Credits weight the GPA."""
        results = [ModuleResult("A", 3, 90), ModuleResult("B", 1, 60)]
        self.assertEqual(calculate_gpa(results), 3.75)

    def test_no_modules(self):
        """No modules means a GPA of zero."""
        self.assertEqual(calculate_gpa([]), 0.0)

    def test_failed(self):
        """Only F grades count as failed."""
        results = [ModuleResult("A", 3, 30), ModuleResult("B", 3, 41)]
        self.assertEqual(failed_modules(results), ["A"])

    def test_class(self):
        """Degree class thresholds."""
        self.assertEqual(class_for_gpa(3.8), "First Class")
        self.assertEqual(class_for_gpa(1.5), "Fail")

    def test_weighted_average(self):
        """Credits weight the average mark."""
        results = [ModuleResult("A", 3, 80), ModuleResult("B", 1, 40)]
        self.assertEqual(weighted_average(results), 70.0)
        self.assertEqual(weighted_average([]), 0.0)

    def test_best_module(self):
        """Highest mark wins, empty list gives None."""
        results = [ModuleResult("A", 3, 55), ModuleResult("B", 2, 81)]
        self.assertEqual(best_module(results).code, "B")
        self.assertIsNone(best_module([]))


if __name__ == "__main__":
    unittest.main()
