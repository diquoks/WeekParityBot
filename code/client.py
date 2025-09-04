from __future__ import annotations
import datetime, logging, telebot
import data, utils, misc


class Client(telebot.TeleBot):
    class ExceptionHandler(telebot.ExceptionHandler):
        def __init__(self, parent: Client) -> None:
            self._logger = parent._logger
            super().__init__()

        def handle(self, e) -> bool:
            self._logger.log_exception(e)
            return True

    def __init__(self) -> None:
        self._config = data.ConfigProvider()
        self._buttons = misc.ButtonsContainer()
        self._logger = data.LoggerService(name=__name__, level=logging.INFO)
        self._exception_handler = self.ExceptionHandler(self)
        super().__init__(
            token=self._config.settings.token,
            exception_handler=self._exception_handler,
        )
        self.register_message_handler(callback=self.info, commands=["start"])
        self.register_message_handler(callback=self.info, commands=["info"])
        self.register_message_handler(callback=self.add_buttons, commands=["add_buttons"])
        self.register_callback_query_handler(callback=self.callback, func=lambda *args: True)

        self._time_started = datetime.datetime.now()
        self._logger.info(f"{self.user.full_name} initialized!")

    @staticmethod
    def get_message_thread_id(message: telebot.types.Message) -> int | None:
        if message.reply_to_message and message.reply_to_message.is_topic_message:
            return message.reply_to_message.message_thread_id
        elif message.is_topic_message:
            return message.message_thread_id
        else:
            return None

    def polling_thread(self) -> None:
        while True:
            try:
                self.polling(non_stop=True)
            except Exception as e:
                self._logger.log_exception(e)

    def add_buttons(self, message: telebot.types.Message) -> None:
        self._logger.log_user_interaction(message.from_user, message.text)

        if message.reply_to_message and message.reply_to_message.document:
            file_path = self.get_file(file_id=message.reply_to_message.document.file_id).file_path
            photo = self.download_file(file_path)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(self._buttons.view_parity)
            markup.row(self._buttons.report_error)
            self.send_photo(
                chat_id=message.chat.id,
                message_thread_id=self.get_message_thread_id(message),
                photo=photo,
                caption=message.reply_to_message.html_caption,
                reply_markup=markup,
            )
        elif message.reply_to_message and message.reply_to_message.photo:
            self.send_message(
                chat_id=message.chat.id,
                message_thread_id=self.get_message_thread_id(message),
                text="Фото должно быть\nотправлено без сжатия!",
            )
        else:
            self.send_message(
                chat_id=message.chat.id,
                message_thread_id=self.get_message_thread_id(message),
                text="Ответьте на сообщение с фото,\nчтобы добавить ему кнопки!",
            )

    def info(self, message: telebot.types.Message) -> None:
        self._logger.log_user_interaction(message.from_user, message.text)

        self.send_message(
            chat_id=message.chat.id,
            message_thread_id=self.get_message_thread_id(message),
            text=f"Информация о {self.user.full_name}:\n\nЗапущен: {self._time_started.strftime("%d.%m.%y %H:%M:%S")} UTC\n\nИсходный код на GitHub:\nhttps://github.com/diquoks/WeekParityBot",
        )

    def callback(self, call: telebot.types.CallbackQuery) -> None:
        self._logger.log_user_interaction(call.from_user, call.data)

        try:
            if call.data == "view_parity":
                self.answer_callback_query(
                    callback_query_id=call.id,
                    text=utils.get_week_parity(),
                    show_alert=True,
                )
        except Exception as e:
            self._logger.log_exception(e)
        finally:
            self.answer_callback_query(callback_query_id=call.id)
