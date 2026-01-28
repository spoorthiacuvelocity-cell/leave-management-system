from datetime import date

COMPANY_HOLIDAYS = [
    date(2026, 1, 15),  # Makara Sankranthi
    date(2026, 1, 26),  # Republic Day
    date(2026, 8, 15),  # Independence Day
    date(2026, 3, 19),  # ugadi
    date(2026, 5, 1),   # May Day
    date(2026, 9, 14),  # Varasiddhi vinayaka vratha
    date(2026, 10, 2),  # Gandhi Jayanthi
    date(2026, 10, 20),  # Ayudhapooja
    date(2026, 10, 21),  # Vijayadasami
    date(2026, 11, 10),  # Deepavi
    date(2026, 12, 25),  # Christmas
]

def is_invalid_leave_day(check_date: date) -> bool:
    # Weekend check
    if check_date.weekday() in (5, 6):  # Saturday, Sunday
        return True

    # Holiday check
    if check_date in COMPANY_HOLIDAYS:
        return True

    return False
