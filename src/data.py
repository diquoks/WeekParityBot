from __future__ import annotations
import aiogram
import pyquoks.data


# region Named classes

class ConfigProvider(pyquoks.data.IConfigProvider):
    class SettingsConfig(pyquoks.data.IConfigProvider.IConfig):
        _SECTION = "Settings"
        bot_token: str
        file_logging: bool
        report_link: str
        skip_updates: bool

    _CONFIG_VALUES = {
        "Settings":
            {
                "bot_token": str,
                "file_logging": bool,
                "report_link": str,
                "skip_updates": bool,
            },
    }
    _CONFIG_OBJECTS = {
        "settings": SettingsConfig,
    }
    settings: SettingsConfig


class LoggerService(pyquoks.data.LoggerService):
    def log_user_interaction(self, user: aiogram.types.User, interaction: str) -> None:
        user_info = f"@{user.username} ({user.id})" if user.username else user.id
        self.info(f"{user_info} - \"{interaction}\"")

# endregion
