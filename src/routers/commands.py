from __future__ import annotations
import datetime
import aiogram, aiogram.filters, pyquoks
import dispatcher as dp, data, utils


class CommandsRouter(aiogram.Router):
    def __init__(self, logger: data.LoggerService) -> None:
        self._logger = logger

        super().__init__(
            name=self.__class__.__name__,
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

        self._logger.info(f"{self.name} initialized!")

    # region Handlers

    async def add_buttons_handler(
            self,
            message: aiogram.types.Message,
            command: aiogram.filters.CommandObject,
            dispatcher: dp.AiogramDispatcher,
    ) -> None:
        self._logger.log_user_interaction(message.from_user, command.text)

        if message.reply_to_message and message.reply_to_message.photo:

            await dispatcher._bot.send_photo(
                chat_id=message.chat.id,
                message_thread_id=utils.get_message_thread_id(message),
                photo=message.reply_to_message.photo[0].file_id,
                caption=message.reply_to_message.html_text,
                reply_markup=dispatcher._keyboards.add_buttons,
            )
        else:
            await dispatcher._bot.send_message(
                chat_id=message.chat.id,
                message_thread_id=utils.get_message_thread_id(message),
                text=dispatcher._strings.menu.add_buttons,
            )

    async def info_handler(
            self,
            message: aiogram.types.Message,
            command: aiogram.filters.CommandObject,
            dispatcher: dp.AiogramDispatcher,
    ) -> None:
        self._logger.log_user_interaction(message.from_user, command.text)

        await dispatcher._bot.send_message(
            chat_id=message.chat.id,
            message_thread_id=utils.get_message_thread_id(message),
            text=dispatcher._strings.menu.info(
                bot_full_name=(await dispatcher._bot.me()).full_name,
                time_started=pyquoks.utils.get_started_datetime().astimezone(
                    tz=datetime.UTC,
                ),
            ),
            reply_markup=dispatcher._keyboards.info,
        )

    # endregion
