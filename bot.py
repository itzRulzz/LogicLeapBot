import time
import logging

from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

# Кнопки
button_duties = KeyboardButton ('О ваших обязанностях')
duties_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_duties)
button_office = KeyboardButton ('О вашем офисе')
office_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_office)
button_colleagues = KeyboardButton ('О ваших коллегах')
colleagues_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_colleagues)
button_company = KeyboardButton ('О компании и ее продуктах')
company_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_company)
button_code = KeyboardButton ('Сменить код должности')
code_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_code)

markup = ReplyKeyboardMarkup().add(button_duties).add(button_office).add(button_colleagues).add(button_company).add(button_code)

# Константы
TOKEN = "5686544173:AAG2P09lCB44aQ-XNWdntDXzEd0_Wiqunf0"
bot = Bot(token=TOKEN) # Принимает наш токен
dp = Dispatcher(bot=bot) # Установка связи с Telegram Bot API
vacation_codes = ['390360', '214667', '075772'] # Коды должностей
class UserState(StatesGroup):
    code_check = State()
    main_menu = State()

# Хэндлер просьбы о вводе кода, /start
@dp.message_handler(commands=['start'])
async def start_welcome(message: types.Message, state: UserState):
    user_full_name = message.from_user.full_name
    logging.info(f'{user_full_name=} {time.asctime()}')
    await message.reply(f"Здравствуй, {user_full_name}, введи код твоей должности чтобы продолжить (обратись к своему тимлиду, если тебе его не дали): ")
    await UserState.code_check.set()

# Хэндлер проверки правильности кода должности
@dp.message_handler()
async def check_code(message: types.Message, state: UserState):
    user_code = message.text
    if user_code in vacation_codes:
        await message.reply("Правильно!")
        await state.update_data(code_checked=True)
        # После успешной проверки кода отправляем пользователю обычное сообщение
        await message.answer ("Добро пожаловать на должность {Текстовый код должности} в компанию LogicLeap. \r\nМы рады привествовать тебя!\r\n", reply_markup=markup)
        await message.answer("Что бы ты хотел узнать?")
        await UserState.main_menu.set()
    else:
        await message.reply("Неправильно!")

# Хэндлер неизвестных команд и сообщений
@dp.message_handler()
async def main_menu(message: types.Message, state: UserState):
    user_data = await state.get_data()
    if user_data.get('code_checked'):
        if message.text == "О ваших обязанностях":
            # Если код еще не проверен, то сообщаем пользователю о необходимости его ввести
            await message.reply("ТЕСТ")
        else:
            # Если код уже проверен, то отправляем пользователю обычное сообщение
            await message.reply("Извините, я не понимаю ваш запрос. Что бы ты хотел узнать?", reply_markup=markup)
    else:
        await message.reply("Пожалуйста, введите код вашей должности, чтобы продолжить.")

"""
@dp.message_handler(text='О ваших обязанностях')
async def echo(message: types.Message):
    await message.answer('testtest')
"""

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)