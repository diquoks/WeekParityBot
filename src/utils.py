from __future__ import annotations
import datetime


def get_formatted_date(date: datetime.datetime) -> str:
    return date.strftime(
        format="%d.%m.%y %H:%M:%S",
    )


def get_week_parity(date: datetime.datetime) -> str:
    current_week_number = date.isocalendar().week

    first_school_week_number = datetime.datetime(
        year=date.year - 1 if current_week_number < datetime.datetime(
            year=date.year - 1,
            month=9,
            day=1,
        ).isocalendar().week else date.year,
        month=9,
        day=1,
    ).isocalendar().week

    last_year_week_number = datetime.datetime(
        year=date.year - 1 if current_week_number < datetime.datetime(
            year=date.year - 1,
            month=12,
            day=28,
        ).isocalendar().week else date.year,
        month=12,
        day=28,
    ).isocalendar().week

    school_week_number = {
        True: current_week_number - first_school_week_number + 1,
        False: last_year_week_number - first_school_week_number + current_week_number + 1,
    }.get(first_school_week_number <= current_week_number)

    return (
        "Сейчас {0} неделя\n"
        "({1} неделя, {2})\n"
    ).format(
        *{
            True: ("зелёная", school_week_number, "чётная"),
            False: ("жёлтая", school_week_number, "нечётная"),
        }.get(school_week_number % 2 == 0)
    )
