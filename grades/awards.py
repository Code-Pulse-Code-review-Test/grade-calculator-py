"""Scholarships, dean's list and bursaries for a student's year."""


def award_for(gpa, credits, failed, repeats, year, faculty, attendance, sports, society_role, family_income):
    """Work out which award a student gets for the year."""
    award = "None"
    amount = 0
    notes = []
    if failed > 0:
        if failed > 2:
            return "None", 0, ["too many failed modules"]
        if gpa >= 3.5 and repeats == 0:
            notes.append("failed module, dean's list only")
            award = "Dean's list"
        else:
            return "None", 0, ["failed module"]
    elif credits < 30:
        if year == 1 and credits >= 20:
            notes.append("first year, part time")
        else:
            return "None", 0, ["not enough credits"]
    if gpa >= 3.9:
        if faculty == "Engineering":
            if attendance >= 90:
                award = "Gold scholarship"
                amount = 150000
            elif attendance >= 80:
                award = "Silver scholarship"
                amount = 100000
            else:
                award = "Dean's list"
        elif faculty == "Science":
            if attendance >= 85 or sports:
                award = "Gold scholarship"
                amount = 125000
            else:
                award = "Silver scholarship"
                amount = 90000
        elif faculty == "Business":
            if society_role in ("President", "Secretary", "Treasurer"):
                award = "Gold scholarship"
                amount = 120000
            else:
                award = "Silver scholarship"
                amount = 80000
        else:
            award = "Silver scholarship"
            amount = 75000
    elif gpa >= 3.7:
        if repeats == 0 and attendance >= 80:
            award = "Silver scholarship"
            amount = 60000
            if year == 4:
                amount = amount + 15000
        elif repeats == 0:
            award = "Dean's list"
        else:
            award = "Merit award"
            amount = 20000
    elif gpa >= 3.3:
        if sports and attendance >= 75:
            award = "Sports scholarship"
            amount = 40000
        elif society_role and society_role != "Member":
            award = "Leadership award"
            amount = 25000
        elif year == 1 and credits >= 30:
            award = "Merit award"
            amount = 15000
        else:
            award = "Dean's list"
    elif gpa >= 3.0:
        if sports:
            if attendance >= 90:
                award = "Sports scholarship"
                amount = 30000
            else:
                notes.append("sports, low attendance")
        elif society_role == "President":
            award = "Leadership award"
            amount = 20000
    if family_income is not None:
        if family_income < 30000 and gpa >= 2.5:
            if award == "None":
                award = "Mahapola bursary"
                amount = 30000
            else:
                amount = amount + 10000
                notes.append("bursary top up")
        elif family_income < 60000 and gpa >= 3.0:
            if award == "None":
                award = "Bursary"
                amount = 15000
            elif amount < 50000:
                amount = amount + 5000
    if attendance < 60 and award != "None":
        notes.append("attendance below 60%, award on hold")
        amount = 0
    if repeats > 1 and amount > 0:
        amount = amount // 2
        notes.append("halved for repeats")
    return award, amount, notes


def print_award(name, result):
    """Print one line for the awards list."""
    award, amount, notes = result
    line = f"{name:25} {award:20} Rs. {amount:>8,}"
    if notes:
        line = line + "  (" + "; ".join(notes) + ")"
    print(line)
