"""Read a marks CSV and print a summary."""

import csv
import sys

from grades.gpa import (
    ModuleResult,
    best_module,
    calculate_gpa,
    class_for_gpa,
    failed_modules,
    weighted_average,
)
from grades.grading import letter_grade


def read_results(path):
    """Read rows of code,credits,mark."""
    with open(path, newline="", encoding="utf-8") as handle:
        return [ModuleResult(code, int(credits), float(mark)) for code, credits, mark in csv.reader(handle)]


def main(argv):
    """Entry point."""
    if len(argv) != 2:
        print("usage: python -m grades.cli <marks.csv>")
        return 1

    results = read_results(argv[1])
    for result in results:
        print(f"{result.code:8} {result.mark:5.1f}  {letter_grade(result.mark)}")

    gpa = calculate_gpa(results)
    print(f"\nGPA: {gpa} ({class_for_gpa(gpa)})")
    print(f"Average mark: {weighted_average(results)}")

    best = best_module(results)
    if best:
        print(f"Best module: {best.code} ({best.mark:.1f})")

    failed = failed_modules(results)
    if failed:
        print("Repeat:", ", ".join(failed))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
