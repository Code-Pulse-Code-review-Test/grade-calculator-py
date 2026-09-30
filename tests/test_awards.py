"""Tests for awards."""

import unittest

from grades.awards import award_for


class AwardTest(unittest.TestCase):
    """Scholarships and bursaries."""

    def test_gold_for_engineering(self):
        """Top GPA with good attendance gets gold."""
        award, amount, _ = award_for(3.95, 60, 0, 0, 2, "Engineering", 95, False, None, None)
        self.assertEqual((award, amount), ("Gold scholarship", 150000))

    def test_too_many_failed(self):
        """Three failed modules means no award."""
        self.assertEqual(award_for(3.9, 60, 3, 0, 2, "Science", 90, False, None, None)[0], "None")

    def test_bursary_for_low_income(self):
        """Low income students get a bursary even without a scholarship."""
        award, amount, _ = award_for(2.8, 60, 0, 0, 2, "Arts", 80, False, None, 25000)
        self.assertEqual((award, amount), ("Mahapola bursary", 30000))


if __name__ == "__main__":
    unittest.main()
