"""Read a marks CSV and print a summary."""

import csv
import sys

from grades.gpa import (
    ModuleResult,
    calculate_gpa,
    class_for_gpa,
    effective_grade_point,
    failed_modules,
)
from grades.grading import grade_point, letter_grade


def read_results(path):
    """Read rows of code,credits,mark with an optional attempt number."""
    with open(path, newline="", encoding="utf-8") as handle:
        return [_parse_row(row) for row in csv.reader(handle) if row]


def _parse_row(row):
    code, credits, mark = row[:3]
    attempt = int(row[3]) if len(row) > 3 and row[3].strip() else 1
    return ModuleResult(code, int(credits), float(mark), attempt)


def _attempt_note(result):
    if result.attempt == 1:
        return ""
    if effective_grade_point(result) < grade_point(result.mark):
        return f"  (attempt {result.attempt}, counts as C)"
    return f"  (attempt {result.attempt})"


def main(argv):
    """Entry point."""
    if len(argv) != 2:
        print("usage: python -m grades.cli <marks.csv>")
        return 1

    results = read_results(argv[1])
    for result in results:
        print(f"{result.code:8} {result.mark:5.1f}  {letter_grade(result.mark)}{_attempt_note(result)}")

    gpa = calculate_gpa(results)
    print(f"\nGPA: {gpa} ({class_for_gpa(gpa)})")

    failed = failed_modules(results)
    if failed:
        print("Repeat:", ", ".join(failed))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
