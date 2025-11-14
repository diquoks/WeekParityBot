from __future__ import annotations
import datetime
import aiogram
import pyquoks
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
                f"Запущен: {utils.get_formatted_date(time_started)} UTC\n"
                f"\n"
                f"Исходный код на GitHub:\n"
                f"https://github.com/diquoks/WeekParityBot\n"
            )

    _OBJECTS = {
        "alert": AlertStrings,
        "menu": MenuStrings,
    }

    alert: AlertStrings
    menu: MenuStrings


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
