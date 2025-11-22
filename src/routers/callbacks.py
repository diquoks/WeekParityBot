from __future__ import annotations
import datetime
import aiogram, aiogram.exceptions, aiogram.filters
import dispatcher as dp, data, utils


class CallbacksRouter(aiogram.Router):
    def __init__(self, logger: data.LoggerService) -> None:
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
            dispatcher: dp.AiogramDispatcher,
    ) -> None:
        self._logger.log_user_interaction(call.from_user, call.data)

        try:
            match call.data:
                case "view_parity":
                    await dispatcher._bot.answer_callback_query(
                        callback_query_id=call.id,
                        text=dispatcher._strings.menu.view_parity(
                            date=datetime.datetime.now(),
                        ),
                        show_alert=True,
                    )
                case "export_logs":
                    if dispatcher._config.settings.file_logging:
                        logs_file = self._logger.file

                        await dispatcher._bot.send_document(
                            chat_id=call.message.chat.id,
                            message_thread_id=utils.get_message_thread_id(call.message),
                            document=aiogram.types.BufferedInputFile(
                                file=logs_file.read(),
                                filename=logs_file.name,
                            ),
                        )

                        logs_file.close()
                    else:
                        await dispatcher._bot.answer_callback_query(
                            callback_query_id=call.id,
                            text=dispatcher._strings.alert.export_logs_unavailable,
                            show_alert=True,
                        )
                case _:
                    await dispatcher._bot.answer_callback_query(
                        callback_query_id=call.id,
                        text=dispatcher._strings.alert.button_unavailable,
                        show_alert=True,
                    )
        except Exception as exception:
            if exception is not aiogram.exceptions.TelegramBadRequest:
                self._logger.log_error(
                    exception=exception,
                )
        finally:
            await dispatcher._bot.answer_callback_query(
                callback_query_id=call.id,
            )

    # endregion
