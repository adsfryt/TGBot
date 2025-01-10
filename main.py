import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

#7927039295:AAGIGFAmnITLGaYixtZ7yQs0jJ2sXgt6V5w - @exampleprojtestbot
#5967619087:AAFLTkBKvi9cKbSDw7sKLrXEuy36fC6Msyw - @KeftemeGoldaBot

async def main():
    bot = Bot(token='7927039295:AAGIGFAmnITLGaYixtZ7yQs0jJ2sXgt6V5w')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')


