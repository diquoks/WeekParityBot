from __future__ import annotations
import datetime
import aiogram, aiogram.utils.keyboard, pyquoks
import utils


# region Providers

class StringsProvider(pyquoks.data.StringsProvider):
    class AlertStrings(pyquoks.data.StringsProvider.Strings):
        @property
        def export_logs_unavailable(self) -> str:
            return "Логирование отключено!"

        @property
        def button_unavailable(self) -> str:
            return "Эта кнопка недоступна!"

    class ButtonStrings(pyquoks.data.StringsProvider.Strings):
        @property
        def view_parity(self) -> str:
            return "Узнать цвет недели"

        @property
        def report_error(self) -> str:
            return "Сообщить об ошибке"

        @property
        def export_logs(self) -> str:
            return "Экспортировать логи"

    class MenuStrings(pyquoks.data.StringsProvider.Strings):
        @property
        def add_buttons(self) -> str:
            return (
                "Ответьте на сообщение с фото,\n"
                "чтобы добавить ему кнопки!\n"
            )

        @staticmethod
        def info(bot_full_name: str, time_started: datetime.datetime) -> str:
            return (
                f"Информация о {bot_full_name}:\n"
                f"\n"
                f"Запущен: {time_started.strftime("%d.%m.%y %H:%M:%S")} UTC\n"
                f"\n"
                f"Исходный код на GitHub:\n"
                f"https://github.com/diquoks/WeekParityBot\n"
            )

        @staticmethod
        def view_parity(date: datetime.datetime) -> str:
            current_week_number = utils.get_week_number(date)

            if current_week_number % 2 == 0:
                current_week_color, current_week_parity = ("зелёная", "чётная")
            else:
                current_week_color, current_week_parity = ("жёлтая", "нечётная")

            return (
                f"Сейчас {current_week_color} неделя\n"
                f"({current_week_number} неделя, {current_week_parity})\n"
            )

    _OBJECTS = {
        "alert": AlertStrings,
        "button": ButtonStrings,
        "menu": MenuStrings,
    }

    alert: AlertStrings
    button: ButtonStrings
    menu: MenuStrings


class ButtonsProvider:
    def __init__(self) -> None:
        self._strings = StringsProvider()
        self._config = ConfigManager()

    @property
    def view_parity(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.view_parity,
            callback_data="view_parity",
        )

    @property
    def report_error(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.report_error,
            url=self._config.settings.report_link,
        )

    @property
    def export_logs(self) -> aiogram.types.InlineKeyboardButton:
        return aiogram.types.InlineKeyboardButton(
            text=self._strings.button.export_logs,
            callback_data="export_logs",
        )


class KeyboardProvider:
    def __init__(self) -> None:
        self._buttons = ButtonsProvider()

    @property
    def add_buttons(self) -> aiogram.types.InlineKeyboardMarkup:
        markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
        markup_builder.row(self._buttons.view_parity)
        markup_builder.row(self._buttons.report_error)

        return markup_builder.as_markup()

    @property
    def info(self) -> aiogram.types.InlineKeyboardMarkup:
        markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
        markup_builder.row(self._buttons.export_logs)

        return markup_builder.as_markup()


# endregion

# region Managers

class ConfigManager(pyquoks.data.ConfigManager):
    class SettingsConfig(pyquoks.data.ConfigManager.Config):
        _SECTION = "Settings"

        _VALUES = {
            "bot_token": str,
            "file_logging": bool,
            "report_link": str,
            "skip_updates": bool,
        }

        bot_token: str
        file_logging: bool
        report_link: str
        skip_updates: bool

    _OBJECTS = {
        "settings": SettingsConfig,
    }

    settings: SettingsConfig


# endregion

# region Services

class LoggerService(pyquoks.data.LoggerService):
    def log_user_interaction(self, user: aiogram.types.User, interaction: str) -> None:
        user_info = f"@{user.username} ({user.id})" if user.username else user.id
        self.info(f"{user_info} - \"{interaction}\"")

# endregion
