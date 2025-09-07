from __future__ import annotations
import datetime, logging, aiogram, aiogram.filters, aiogram.client.default, aiogram.client.session.aiohttp
import data, utils, misc


class AiogramClient(aiogram.Dispatcher):
    def __init__(self):
        self._config = data.ConfigProvider()
        self._buttons = misc.ButtonsContainer()
        self._logger = data.LoggerService(
            name=__name__,
            level=logging.INFO,
        )
        if self._config.settings.use_pythonanywhere_proxy:
            session = aiogram.client.session.aiohttp.AiohttpSession(proxy="http://proxy.server:3128")
        else:
            session = None
        self._bot = aiogram.Bot(
            token=self._config.settings.bot_token,
            session=session,
            default=aiogram.client.default.DefaultBotProperties(
                parse_mode=aiogram.enums.ParseMode.HTML,
            ),
        )
        self._bot_name = None
        super().__init__(name="WeekParityDispatcher")
        self.errors.register(self.handle_error)
        self.message.register(self.info, aiogram.filters.Command("start", "info"))
        self.message.register(self.add_buttons, aiogram.filters.Command("add_buttons"))
        self.callback_query.register(self.callback)

        self._time_started = datetime.datetime.now(tz=datetime.timezone.utc)
        self._logger.info(f"{self.name} initialized!")

    @property
    async def bot_name(self):
        if not self._bot_name:
            self._bot_name = (await self._bot.get_my_name()).name
        return self._bot_name

    @staticmethod
    def get_message_thread_id(message: aiogram.types.Message) -> int | None:
        if message.reply_to_message and message.reply_to_message.is_topic_message:
            return message.reply_to_message.message_thread_id
        elif message.is_topic_message:
            return message.message_thread_id
        else:
            return None

    async def handle_error(self, event: aiogram.types.ErrorEvent) -> None:
        self._logger.log_exception(event.exception)

    async def polling_coroutine(self) -> None:
        try:
            await self.start_polling(self._bot)
        except Exception as e:
            self._logger.log_exception(e)

    async def add_buttons(self, message: aiogram.types.Message) -> None:
        self._logger.log_user_interaction(message.from_user, message.text)

        if message.reply_to_message and message.reply_to_message.photo:
            markup = aiogram.types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [self._buttons.view_parity],
                    [self._buttons.report_error],
                ],
            )
            await self._bot.send_photo(
                chat_id=message.chat.id,
                message_thread_id=self.get_message_thread_id(message),
                photo=message.reply_to_message.photo[0].file_id,
                caption=message.reply_to_message.html_text,
                reply_markup=markup,
            )
        else:
            await self._bot.send_message(
                chat_id=message.chat.id,
                message_thread_id=self.get_message_thread_id(message),
                text="Ответьте на сообщение с фото,\nчтобы добавить ему кнопки!",
            )

    async def info(self, message: aiogram.types.Message) -> None:
        self._logger.log_user_interaction(message.from_user, message.text)

        await self._bot.send_message(
            chat_id=message.chat.id,
            message_thread_id=self.get_message_thread_id(message),
            text=f"Информация о {await self.bot_name}:\n\nЗапущен: {self._time_started.strftime("%d.%m.%y %H:%M:%S")} UTC\n\nИсходный код на GitHub:\nhttps://github.com/diquoks/WeekParityBot"
        )

    async def callback(self, call: aiogram.types.CallbackQuery) -> None:
        self._logger.log_user_interaction(call.from_user, call.data)

        try:
            if call.data == "view_parity":
                await self._bot.answer_callback_query(
                    callback_query_id=call.id,
                    text=utils.get_week_parity(),
                    show_alert=True,
                )
        except Exception as e:
            self._logger.log_exception(e)
        finally:
            await self._bot.answer_callback_query(callback_query_id=call.id)
