from __future__ import annotations
import aiogram
import data


class ButtonsContainer:
    def __init__(self) -> None:
        self._config = data.ConfigProvider()

        # region /add_buttons

        self.view_parity = aiogram.types.InlineKeyboardButton(
            text="Узнать цвет недели",
            callback_data="view_parity",
        )
        self.report_error = aiogram.types.InlineKeyboardButton(
            text="Сообщить об ошибке",
            url=self._config.settings.report_link,
        )

        # endregion

        # region /info

        self.export_logs = aiogram.types.InlineKeyboardButton(
            text="Экспортировать логи",
            callback_data="export_logs",
        )

        # endregion
