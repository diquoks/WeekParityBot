from __future__ import annotations
import datetime, logging
import aiogram, aiogram.exceptions, aiogram.filters, aiogram.client.default, aiogram.utils.keyboard
import data, utils, misc


class AiogramClient(aiogram.Dispatcher):
    _COMMANDS = [
        aiogram.types.BotCommand(command="/add_buttons", description="Добавить кнопки к расписанию"),
        aiogram.types.BotCommand(command="/info", description="Информация о боте"),
    ]

    def __init__(self) -> None:
        self._user = None
        self._config = data.ConfigManager()
        self._strings = data.StringsProvider()
        self._logger = data.LoggerService(
            filename=__name__,
            file_handling=self._config.settings.file_logging,
            level=logging.INFO,
        )
        self._buttons = misc.ButtonsContainer()
        self._bot = aiogram.Bot(
            token=self._config.settings.bot_token,
            default=aiogram.client.default.DefaultBotProperties(
                parse_mode=aiogram.enums.ParseMode.HTML,
            ),
        )
        super().__init__(name="WeekParityDispatcher")

        self.errors.register(
            self.error_handler,
        )
        self.startup.register(
            self.startup_handler,
        )
        self.shutdown.register(
            self.shutdown_handler,
        )
        self.message.register(
            self.add_buttons_handler,
            aiogram.filters.Command(
                "add_buttons",
            ),
        )
        self.message.register(
            self.info_handler,
            aiogram.filters.Command(
                "start",
                "info",
            ),
        )
        self.callback_query.register(
            self.callback_handler,
        )

        self._time_started = datetime.datetime.now(tz=datetime.timezone.utc)
        self._logger.info(f"{self.name} initialized!")

    # region Properties and helpers

    @property
    async def user(self) -> aiogram.types.User:
        if not self._user:
            self._user = (await self._bot.get_me())
        return self._user

    @staticmethod
    def _get_message_thread_id(message: aiogram.types.Message) -> int | None:
        if message.reply_to_message and message.reply_to_message.is_topic_message:
            return message.reply_to_message.message_thread_id
        elif message.is_topic_message:
            return message.message_thread_id
        else:
            return None

    async def polling_coroutine(self) -> None:
        try:
            await self._bot.delete_webhook(drop_pending_updates=self._config.settings.skip_updates)
            await self.start_polling(self._bot)
        except Exception as exception:
            self._logger.log_error(
                exception=exception,
            )

    # endregion

    # region Handlers

    async def error_handler(self, event: aiogram.types.ErrorEvent) -> None:
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

    async def add_buttons_handler(self, message: aiogram.types.Message, command: aiogram.filters.CommandObject) -> None:
        self._logger.log_user_interaction(message.from_user, command.text)

        if message.reply_to_message and message.reply_to_message.photo:
            markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
            markup_builder.row(self._buttons.view_parity)
            markup_builder.row(self._buttons.report_error)

            await self._bot.send_photo(
                chat_id=message.chat.id,
                message_thread_id=self._get_message_thread_id(message),
                photo=message.reply_to_message.photo[0].file_id,
                caption=message.reply_to_message.html_text,
                reply_markup=markup_builder.as_markup(),
            )
        else:
            await self._bot.send_message(
                chat_id=message.chat.id,
                message_thread_id=self._get_message_thread_id(message),
                text=self._strings.menu.add_buttons,
            )

    async def info_handler(self, message: aiogram.types.Message, command: aiogram.filters.CommandObject) -> None:
        self._logger.log_user_interaction(message.from_user, command.text)

        markup_builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
        markup_builder.row(self._buttons.export_logs)

        await self._bot.send_message(
            chat_id=message.chat.id,
            message_thread_id=self._get_message_thread_id(message),
            text=self._strings.menu.info(
                bot_full_name=(await self.user).full_name,
                time_started=self._time_started,
            ),
            reply_markup=markup_builder.as_markup(),
        )

    async def callback_handler(self, call: aiogram.types.CallbackQuery) -> None:
        self._logger.log_user_interaction(call.from_user, call.data)

        try:
            match call.data:
                case "view_parity":
                    await self._bot.answer_callback_query(
                        callback_query_id=call.id,
                        text=utils.get_week_parity(
                            date=datetime.datetime.now(),
                        ),
                        show_alert=True,
                    )
                case "export_logs":
                    if self._config.settings.file_logging:
                        logs_file = self._logger.file

                        await self._bot.send_document(
                            chat_id=call.message.chat.id,
                            message_thread_id=self._get_message_thread_id(message=call.message),
                            document=aiogram.types.BufferedInputFile(
                                file=logs_file.read(),
                                filename=logs_file.name,
                            ),
                        )

                        logs_file.close()
                    else:
                        await self._bot.answer_callback_query(
                            callback_query_id=call.id,
                            text=self._strings.alert.export_logs_unavailable,
                            show_alert=True,
                        )
                case _:
                    await self._bot.answer_callback_query(
                        callback_query_id=call.id,
                        text=self._strings.alert.button_unavailable,
                        show_alert=True,
                    )
        except Exception as exception:
            if exception is not aiogram.exceptions.TelegramBadRequest:
                self._logger.log_error(
                    exception=exception,
                )
        finally:
            await self._bot.answer_callback_query(callback_query_id=call.id)

    # endregion
