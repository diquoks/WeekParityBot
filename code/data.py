from __future__ import annotations
import configparser, datetime, logging, aiogram, sys, os


class ConfigProvider:
    """
    :var settings: ``SettingsConfig``
    """

    class IConfig:
        _SECTION: str = None
        _CONFIG_VALUES: set = None

        def __init__(self, parent: ConfigProvider = None) -> None:
            if isinstance(parent, ConfigProvider):
                self._CONFIG_VALUES = parent._CONFIG_VALUES[self._SECTION]
                self._incorrect_content_exception = configparser.ParsingError("config.ini is filled incorrectly!")
                self._config = configparser.ConfigParser()
                self._config.read("config.ini")
                if not self._config.has_section(self._SECTION):
                    self._config.add_section(self._SECTION)
                for i in self._CONFIG_VALUES:
                    try:
                        setattr(self, i, self._config.get(self._SECTION, i))
                    except:
                        self._config.set(self._SECTION, i, i)
                        with open("config.ini", "w") as file:
                            self._config.write(fp=file)
                if not self.values:
                    raise self._incorrect_content_exception

        @property
        def values(self) -> dict | None:
            try:
                return {i: getattr(self, i) for i in self._CONFIG_VALUES}
            except:
                return None

    class SettingsConfig(IConfig):
        """
        :var bot_token: ``str``
        :var report_link: ``str``
        :var use_pythonanywhere_proxy: ``bool``
        """

        _SECTION = "Settings"
        bot_token: str | None
        report_link: str | None
        use_pythonanywhere_proxy: bool | str | None

        def __init__(self, parent: ConfigProvider) -> None:
            super().__init__(parent=parent)
            # bool variables
            for i in ["use_pythonanywhere_proxy"]:
                if getattr(self, i) not in [str(True), str(False)]:
                    setattr(self, i, None)
                    raise self._incorrect_content_exception
                else:
                    setattr(self, i, getattr(self, i) == str(True))

    _CONFIG_VALUES = {
        "Settings":
            {
                "bot_token",
                "report_link",
                "use_pythonanywhere_proxy",
            },
    }

    def __init__(self) -> None:
        self.settings = self.SettingsConfig(self)
        super().__init__()


class LoggerService(logging.Logger):
    def __init__(self, name: str, file_handling: bool = True, filename: str = datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S"), level: int = logging.NOTSET, folder_name: str = "logs") -> None:
        super().__init__(name, level)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter(fmt="$levelname $asctime $name - $message", datefmt="%d-%m-%y %H:%M:%S", style="$"))
        self.handlers.append(stream_handler)
        if file_handling:
            os.makedirs(folder_name, exist_ok=True)
            file_handler = logging.FileHandler(f"{folder_name}/{filename}-{name}.log", encoding="utf-8")
            file_handler.setFormatter(logging.Formatter(fmt="$levelname $asctime - $message", datefmt="%d-%m-%y %H:%M:%S", style="$"))
            self.handlers.append(file_handler)

    def log_user_interaction(self, user: aiogram.types.User, interaction: str) -> None:
        user_info = f"@{user.username} ({user.id})" if user.username else user.id
        self.info(f"{user_info} - \"{interaction}\"")

    def log_exception(self, e: Exception) -> None:
        self.error(msg=e, exc_info=True)
