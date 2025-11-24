from __future__ import annotations

import datetime

import aiogram


def get_message_thread_id(message: aiogram.types.Message) -> int | None:
    if message.reply_to_message and message.reply_to_message.is_topic_message:
        return message.reply_to_message.message_thread_id
    elif message.is_topic_message:
        return message.message_thread_id
    else:
        return None


def get_week_number(date: datetime.datetime) -> int:
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

    if first_school_week_number <= current_week_number:
        return current_week_number - first_school_week_number + 1
    else:
        return last_year_week_number - first_school_week_number + current_week_number + 1
