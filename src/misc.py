from __future__ import annotations
import aiogram
import data


class ButtonsContainer:
    def __init__(self) -> None:
        self._config = data.ConfigManager()

    # region /add_buttons

    @property
    def view_parity(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text="Узнать цвет недели",
            callback_data="view_parity",
        )

    @property
    def report_error(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text="Сообщить об ошибке",
            url=self._config.settings.report_link,
        )

    # endregion

    # region /info

    @property
    def export_logs(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text="Экспортировать логи",
            callback_data="export_logs",
        )

    # endregion
