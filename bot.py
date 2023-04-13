import time
import logging

from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

""""
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
"""

# Кнопки
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add('О ваших обязанностях').add('О вашем офисе').add('О ваших коллегах').add('О компании и ее продуктах')

# Константы
TOKEN = "5686544173:AAG2P09lCB44aQ-XNWdntDXzEd0_Wiqunf0"
bot = Bot(token=TOKEN) # Принимает наш токен
dp = Dispatcher(bot=bot) # Установка связи с Telegram Bot API
vacation_codes = ['390360', '214667', '075772'] # Коды должностей
office_text1 = """
Добро пожаловать в наш офис компании! Мы гордимся нашим современным и просторным офисом, который был специально разработан и оборудован с целью обеспечить комфортную и продуктивную рабочую среду для каждого из наших сотрудников.

Наш офис разделен на несколько функциональных зон, включая рабочие зоны, зоны отдыха, зоны для проведения встреч и переговорных комнат, а также зоны для питания и кухни. Мы также предлагаем нашим сотрудникам доступ к бесплатной кафе и кофейни в офисе с широким выбором напитков и закусок.
"""
office_text2 = """
Мы полагаем, что технологии – ключевое средство, которое позволяет нам оставаться конкурентными и увеличивать результативность работы каждого из наших сотрудников. Поэтому мы предлагаем современное оборудование и программное обеспечение для всех наших сотрудников.

Мы также организуем различные события и мероприятия, чтобы наши сотрудники могли сблизиться, обменяться идеями и отдохнуть от работы. Наши инициативы включают в себя спортивные соревнования, корпоративные вечера и многое другое.

Надеемся, что наш офис окажется для тебя приятным, комфортным и эффективным местом работы. С нетерпением ждем нашей продуктивной работы вместе!
"""
company_and_products_text="""
LogicLeap - это быстро растущая компания, которая занимается разработкой и продажей программного обеспечения для малого и среднего бизнеса. Наше ПО помогает нашим клиентам управлять своими бизнесами более эффективно и улучшать свою прибыльность. Мы стремимся стать лидером на рынке программного обеспечения для малого и среднего бизнеса и ищем талантливых людей, которые готовы присоединиться к нам и помочь достичь этой цели. У нас есть дружелюбная и профессиональная команда, которая всегда готова помочь и поддержать новых сотрудников. Если ты ищешь интересную и перспективную работу в IT-сфере, то LogicLeap - идеальное место!

Рад сообщить тебе о товарах, которые мы предлагаем в нашей компании. Мы специализируемся на разработке программного обеспечения на заказ, которое может быть адаптировано для любой отрасли и конкретных требований наших клиентов.

Наша команда состоит из опытных разработчиков, которые могут создать различные типы программного обеспечения, от мобильных приложений до сложных систем управления проектами.

Наша продукция охватывает самые разные области, от образовательных приложений до приложений в области здравоохранения. Например, мы разработали приложение для тренировки памяти и концентрации для студентов, приложение для заказа билетов в кино и приложение для управления забронированными кроватями в больницах.
"""

# Хэндлер просьбы о вводе кода, /start
@dp.message_handler(commands=['start'])
async def start_welcome(message: types.Message):
    user_full_name = message.from_user.full_name
    logging.info(f'{user_full_name=} {time.asctime()}')
    await message.answer(f"Здравствуй, {user_full_name}! С чего начнем?", reply_markup=main_menu) # введи код твоей должности чтобы продолжить (обратись к своему тимлиду, если тебе его не дали): 

# Хэндлер "О вашем офисе"
@dp.message_handler(text='О вашем офисе')
async def about_office(message: types.Message):
    await message.answer_photo(open('imgs\img6.png', 'rb'), caption=office_text1)
    await message.answer(text=office_text2)

# Хэндлер "О компании и ее продуктах"
@dp.message_handler(text='О компании и ее продуктах')
async def company_and_products(message: types.Message):
    await message.answer(text=company_and_products_text)

# Хэндлер неизвестных команд
@dp.message_handler()
async def unknow(message: types.Message):
    await message.reply("Неизвестная команда!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
