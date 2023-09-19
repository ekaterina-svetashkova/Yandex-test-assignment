import gspread
from datetime import datetime
import logging

from aiogram import Bot, types, Dispatcher, executor
from config import TOKEN

# определяем подключение к google doc'у
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# путь к json-файлу, сгенерированному для подключения к Google Sheets API
credentials = Credentials.from_service_account_file(
    r'../credentials/test-project-399514-91e724ef09fd.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

# ссылка на созданный гугл-док (у service-аккаунта должен быть доступ на запись)
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/146ahYwfP9hueMCP4KQX8xnO6_T-NTYCeQvmiyDlQtPM/edit#gid=323406007')

worksheet = spreadsheet.get_worksheet(0)

# настраиваем логирование
logging.basicConfig(filename="my-logfile.log", format="%(asctime)s - %(message)s", filemode="a", level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler())
logging.warning("Записываются сообщения с предупреждениями.")



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь.")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я запишу это сообщение с датой и логином в Google-таблицу.")


@dp.message_handler()
async def write_message_contents(message: types.Message):
    try:
        l = [message.from_user.username, message.text, message.date]
    except:
        logging.error("Ошибка в обработке данных из сообщения")
    try:
        l[2] = message.date.strftime("%Y-%m-%d %H:%M:%S")
        worksheet.append_row(l)
        await message.reply('Сообщение записано в Google-таблицу')
    except:
        logging.error("Не получилось записать данные в таблицу")

    logging.shutdown()


if __name__ == '__main__':
    executor.start_polling(dp)