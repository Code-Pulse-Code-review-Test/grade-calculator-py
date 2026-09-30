"""Tests for grading and GPA."""

import os
import tempfile
import unittest

from grades.cli import read_results
from grades.gpa import (
    ModuleResult,
    calculate_gpa,
    class_for_gpa,
    effective_grade_point,
    failed_modules,
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


class RepeatTest(unittest.TestCase):
    """Repeat attempts."""

    def test_repeat_capped_at_c(self):
        """A repeat pass counts as a C at most."""
        self.assertEqual(effective_grade_point(ModuleResult("A", 3, 80, attempt=2)), 2.0)
        self.assertEqual(effective_grade_point(ModuleResult("A", 3, 42, attempt=2)), 1.0)

    def test_first_attempt_not_capped(self):
        """The cap only applies from the second attempt."""
        self.assertEqual(effective_grade_point(ModuleResult("A", 3, 80)), 4.0)

    def test_only_latest_attempt_counts(self):
        """A failed first attempt is replaced by the repeat."""
        results = [
            ModuleResult("A", 3, 30),
            ModuleResult("B", 3, 90),
            ModuleResult("A", 3, 75, attempt=2),
        ]
        self.assertEqual(calculate_gpa(results), 3.0)
        self.assertEqual(failed_modules(results), [])


class ReadResultsTest(unittest.TestCase):
    """Reading the marks file."""

    def test_attempt_column_is_optional(self):
        """Rows without an attempt number are first attempts."""
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as handle:
            handle.write("CS1033,3,78\nMA1024,3,71,2\n")
        try:
            results = read_results(handle.name)
        finally:
            os.remove(handle.name)
        self.assertEqual([r.attempt for r in results], [1, 2])


if __name__ == "__main__":
    unittest.main()
