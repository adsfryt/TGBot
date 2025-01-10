from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
#                                      [KeyboardButton(text='Корзина')],
#                                      [KeyboardButton(text='Контакты'), 
#                                       KeyboardButton(text='О нас')]],
#                             resize_keyboard=True,
#                             input_field_placeholder='Выберите пункт меню...')

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Яндекс', callback_data='yandex')],
    [InlineKeyboardButton(text='Github', callback_data='git')],
    [InlineKeyboardButton(text='Код', callback_data='code')]])

#callback_data='yandex'
#callback_data='git'

roles = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Студент', callback_data='student')],
    [InlineKeyboardButton(text='Преподаватель', callback_data='teacher')]])


start_test = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать тест', callback_data='start_test')],
    [InlineKeyboardButton(text='Посмотреть все свои попытки', callback_data='get_all_attempts')] ])

# get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', 
#                                                            request_contact=True)]],
#                                  resize_keyboard=True)

# im_logged = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Я залогинен', callback_data='imlogged')],
#     ])

#command_buttons = InlineKeyboardMarkup(keyboard=[
#    [InlineKeyboardButton(text='/start', callback_data='start')],
#    [InlineKeyboardButton(text='/help', callback_data='help')],
#    [InlineKeyboardButton(text='/register', callback_data='register')]])