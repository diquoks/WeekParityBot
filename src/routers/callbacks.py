from __future__ import annotations
import datetime
import aiogram, aiogram.exceptions, aiogram.filters
import data, utils


class CallbacksRouter(aiogram.Router):
    def __init__(self, logger: data.LoggerService) -> None:
        self._strings = data.StringsProvider()
        self._config = data.ConfigManager()
        self._logger = logger

        super().__init__(
            name=self.__class__.__name__,
        )

        self.callback_query.register(
            self.callback_handler,
        )

        self._logger.info(f"{self.name} initialized!")

    # region Handlers

    async def callback_handler(
            self,
            call: aiogram.types.CallbackQuery,
            bot: aiogram.Bot,
    ) -> None:
        self._logger.log_user_interaction(call.from_user, call.data)

        try:
            match call.data:
                case "view_parity":
                    await bot.answer_callback_query(
                        callback_query_id=call.id,
                        text=self._strings.menu.view_parity(
                            date=datetime.datetime.now(),
                        ),
                        show_alert=True,
                    )
                case "export_logs":
                    if self._config.settings.file_logging:
                        logs_file = self._logger.file

                        await bot.send_document(
                            chat_id=call.message.chat.id,
                            message_thread_id=utils.get_message_thread_id(call.message),
                            document=aiogram.types.BufferedInputFile(
                                file=logs_file.read(),
                                filename=logs_file.name,
                            ),
                        )

                        logs_file.close()
                    else:
                        await bot.answer_callback_query(
                            callback_query_id=call.id,
                            text=self._strings.alert.export_logs_unavailable,
                            show_alert=True,
                        )
                case _:
                    await bot.answer_callback_query(
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
            await bot.answer_callback_query(
                callback_query_id=call.id,
            )

    # endregion
