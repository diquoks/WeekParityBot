from __future__ import annotations
import telebot
import data


class ButtonsContainer:
    def __init__(self):
        self._config = data.ConfigProvider()

        # /send_schedule
        self.view_parity = telebot.types.InlineKeyboardButton(text="Узнать цвет недели", callback_data="view_parity")
        self.report_error = telebot.types.InlineKeyboardButton(text="Сообщить об ошибке", url=self._config.settings.report_link)
