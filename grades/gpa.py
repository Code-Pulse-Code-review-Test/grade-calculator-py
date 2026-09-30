"""GPA over a list of modules."""

from dataclasses import dataclass

from grades.grading import grade_point

# a repeated module can earn at most a C
REPEAT_CAP = 2.0


@dataclass
class ModuleResult:
    """One module with its credits, final mark and attempt number."""

    code: str
    credits: int
    mark: float
    attempt: int = 1


def effective_grade_point(result):
    """Grade point that counts towards the GPA, capped for repeat attempts."""
    point = grade_point(result.mark)
    if result.attempt > 1:
        return min(point, REPEAT_CAP)
    return point


def latest_attempts(results):
    """Keep only the latest attempt of each module."""
    latest = {}
    for result in results:
        current = latest.get(result.code)
        if current is None or result.attempt > current.attempt:
            latest[result.code] = result
    return list(latest.values())


def calculate_gpa(results):
    """Credit-weighted GPA over the latest attempts, rounded to two decimals."""
    counted = latest_attempts(results)
    total_credits = sum(r.credits for r in counted)
    if total_credits == 0:
        return 0.0
    weighted = sum(effective_grade_point(r) * r.credits for r in counted)
    return round(weighted / total_credits, 2)


def failed_modules(results):
    """Codes of modules whose latest attempt is an F."""
    return [r.code for r in latest_attempts(results) if grade_point(r.mark) == 0.0]


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
