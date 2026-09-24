"""GPA over a list of modules."""

from dataclasses import dataclass

from grades.grading import grade_point


@dataclass
class ModuleResult:
    """One module with its credits and final mark."""

    code: str
    credits: int
    mark: float


def calculate_gpa(results):
    """Credit-weighted GPA, rounded to two decimals."""
    total_credits = sum(r.credits for r in results)
    if total_credits == 0:
        return 0.0
    weighted = sum(grade_point(r.mark) * r.credits for r in results)
    return round(weighted / total_credits, 2)


def failed_modules(results):
    """Codes of modules with an F."""
    return [r.code for r in results if grade_point(r.mark) == 0.0]


def class_for_gpa(gpa):
    """Degree class for a final GPA."""
    if gpa >= 3.7:
        return "First Class"
    if gpa >= 3.3:
        return "Second Class (Upper)"
    if gpa >= 3.0:
        return "Second Class (Lower)"
    if gpa >= 2.0:
        return "Pass"
    return "Fail"
