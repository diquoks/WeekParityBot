# WeekParityBot

#### Telegram-бот для добавления расширенного функционала расписаниям

---

## Оглавление

- [Контакты](#контакты)
    - [Связь с разработчиком](#связь-с-разработчиком)
    - [Прочие ссылки](#прочие-ссылки)
- [Сборка и запуск](#сборка-и-запуск)
    - [Необходимые компоненты](#необходимые-компоненты)
    - [Первоначальная настройка](#первоначальная-настройка)
    - [config.ini](#configini)
        - [Раздел `Settings`](#раздел-settings)
    - [Docker](#docker)

---

## Контакты

#### Связь с разработчиком

- [Telegram для связи](https://t.me/diquoks)
- [Почта для связи](mailto:diquoks@yandex.ru)

#### Прочие ссылки

- [Бот в Telegram](https://t.me/week_parity_bot)
- [Telegram-канал с новостями](https://t.me/diquoks_channel)

---

## Сборка и запуск

### Необходимые компоненты

- [Docker Desktop](https://docs.docker.com/desktop)
- [Git](https://git-scm.com/downloads)
- [Python 3.13](https://www.python.org/downloads)

### Первоначальная настройка

##### Клонируйте репозиторий git

```bash
git clone https://github.com/diquoks/WeekParityBot.git
```

##### Перейдите в корневую директорию

```bash
cd WeekParityBot
```

##### Установите зависимости

```bash
pip install -r requirements.txt
```

##### Сгенерируйте файл `config.ini`

```bash
cd src ; python main.py
```

##### Заполните `WeekParityBot/src/config.ini` [следуя инструкции](#configini)

##### Используйте руководство для [Docker](#docker)

### config.ini

#### Раздел `Settings`

| Настройка      |  Тип   | Описание                                      |
|:---------------|:------:|:----------------------------------------------|
| `bot_token`    | `str`  | Токен бота в Telegram                         |
| `file_logging` | `bool` | Использовать логирование в файлы `.log`       |
| `report_link`  | `str`  | Ссылка для связи с администратором бота       |
| `skip_updates` | `bool` | Пропускать ожидающие события при запуске бота |

### Docker

##### Перейдите в корневую директорию

##### Создайте образ

```bash
docker build -t week_parity_bot .
```

##### Запустите контейнер

```bash
docker run -it -d --name WeekParityBot week_parity_bot
```
