from __future__ import annotations

import logging

import aiogram
import aiogram.client.default
import aiogram.exceptions

import data
import routers


class AiogramDispatcher(aiogram.Dispatcher):
    _COMMANDS = [
        aiogram.types.BotCommand(
            command="/add_buttons",
            description="Добавить кнопки к расписанию",
        ),
        aiogram.types.BotCommand(
            command="/info",
            description="Информация о боте",
        ),
    ]

    _IGNORED_EXCEPTIONS = [
        aiogram.exceptions.TelegramForbiddenError,
        aiogram.exceptions.TelegramRetryAfter,
    ]

    def __init__(self) -> None:
        self._strings = data.StringsProvider()
        self._keyboards = data.KeyboardProvider()
        self._config = data.ConfigManager()
        self._logger = data.LoggerService(
            filename=__name__,
            file_handling=self._config.settings.file_logging,
            level=logging.INFO,
        )
        self._bot = aiogram.Bot(
            token=self._config.settings.bot_token,
            default=aiogram.client.default.DefaultBotProperties(
                parse_mode=aiogram.enums.ParseMode.HTML,
            ),
        )

        super().__init__(
            name=self.__class__.__name__,
        )

        self.errors.register(
            self.error_handler,
        )
        self.startup.register(
            self.startup_handler,
        )
        self.shutdown.register(
            self.shutdown_handler,
        )

        self.include_routers(
            routers.commands.CommandsRouter(
                logger=self._logger,
            ),
            routers.callbacks.CallbacksRouter(
                logger=self._logger,
            ),
        )

        self._logger.info(f"{self.name} initialized!")

    # region Helpers

    async def polling_coroutine(self) -> None:
        try:
            await self._bot.delete_webhook(
                drop_pending_updates=self._config.settings.skip_updates,
            )

            await self.start_polling(self._bot)
        except Exception as exception:
            self._logger.log_error(
                exception=exception,
            )

    # endregion

    # region Handlers

    async def error_handler(self, event: aiogram.types.ErrorEvent) -> None:
        if type(event.exception) not in self._IGNORED_EXCEPTIONS:
            self._logger.log_error(
                exception=event.exception,
            )

    async def startup_handler(self) -> None:
        await self._bot.set_my_commands(
            commands=self._COMMANDS,
            scope=aiogram.types.BotCommandScopeDefault(),
        )

        self._logger.info(f"{self.name} started!")

    async def shutdown_handler(self) -> None:
        self._logger.info(f"{self.name} terminated")

    # endregion
