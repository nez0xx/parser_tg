import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from pathlib import Path

from aiogram.types import Message

from parser import parse_excel

BASE_DIR = Path(__file__).parent
print(BASE_DIR)

dp = Dispatcher()


def get_data(filename: str):
    united_orders = parse_excel(filename)
    data = {}
    for united_order in united_orders:
        names = []
        print(united_order["united_order_id"])
        for o in united_order["orders"]:
            name = o["customer"]["name"].split()
            for i in range(len(name)):
                name[i] = name[i].capitalize()
            names.append("🍀"+" ".join(name))
            print("🍀"+" ".join(name))
        names = sorted(list(set(names)))
        data[united_order["united_order_id"]] = names
    return data


@dp.message(F.document)
async def handle_photo_with_please_caption(message: Message, bot: Bot):
    print(message.document.__dict__)
    date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{date}_{message.document.file_name}"
    path = os.path.join(BASE_DIR, f'documents\\{filename}') #там создается папка documents, туда и будут сохраняться файлы
    print(path, "PATH")
    await bot.download(
        message.document,
        destination=path
    )
    text = ""
    data = get_data(path)
    for key in data:
        text += key+"\n"
        for name in data[key]:
            text += name+"\n"
    os.remove(path)
    await message.reply(text)


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token='6857321691:AAHSqOvfWJzqIh3jRO-KhqsgUcChSrxQlJ4',
        # parse_mode=ParseMode.MARKDOWN_V2,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
