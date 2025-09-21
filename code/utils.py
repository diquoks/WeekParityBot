from __future__ import annotations
import datetime


def get_week_parity(date: datetime.datetime = datetime.datetime.now()) -> str:
    first_week = datetime.datetime(
        year=date.year - 1 if date.isocalendar().week < datetime.datetime(
            year=date.year - 1,
            month=9,
            day=1,
        ).isocalendar().week else date.year,
        month=9,
        day=1,
    ).isocalendar().week
    return "Сейчас {0} неделя\n({1})".format(
        *{
            True: ("зелёная", "чётная"),
            False: ("жёлтая", "нечётная"),
        }.get(bool((date.isocalendar().week - first_week) % 2))
    )
