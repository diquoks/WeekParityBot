import asyncio

import dispatcher


async def main() -> None:
    bot = dispatcher.AiogramDispatcher()
    await bot.polling_coroutine()


if __name__ == "__main__":
    asyncio.run(main())
