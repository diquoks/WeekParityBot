from __future__ import annotations
import datetime


def get_week_parity(date: datetime.datetime = datetime.datetime.now()) -> str:
    if date.isocalendar()[1] < datetime.datetime(date.year - 1, 9, 1).isocalendar()[1]:
        week_first = datetime.datetime(date.year - 1, 9, 1).isocalendar()[1]
    else:
        week_first = datetime.datetime(date.year, 9, 1).isocalendar()[1]
    return "Сейчас {0} неделя\n{1}".format(*("зелёная", "(чётная)") if (date.isocalendar()[1] - week_first + 1) % 2 == 0 else ("жёлтая", "(нечётная)"))
