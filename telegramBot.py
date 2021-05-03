import telebot
from telebot import types

bot = telebot.TeleBot('1795585629:AAE08nhtl2w_waeSMrGbg3qIcOjPCam6jLc')

language_from = 'rus'
language_to = 'eng'
def translate(given_word):
    global language_from
    global language_to
    id_from = 1
    id_to = 0
    if language_from == 'rus':
        id_from = 1
    elif language_from == 'eng':
        id_from = 0
    
    if language_to == 'rus':
        id_to = 1
    elif language_to == 'end':
        id_to = 0

    dictionary = dict()
    dictionary['hello'] = 'привет'
    dictionary['world'] = 'мир'
    dictionary['love'] = 'любовь'
    dictionary['bye'] = 'пока'
    dictionary['family'] = 'семья'
    for word in dictionary.items():
        if word[id_from] == given_word:
            return word[id_to]
    return 'Не знаю такого слова, прости('

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Тут можно переводить слова')
        
        keyboard = types.InlineKeyboardMarkup()
        key_rus = types.InlineKeyboardButton(text='Русский', callback_data = 'get_language_rus')
        keyboard.add(key_rus)
        key_eng = types.InlineKeyboardButton(text='English', callback_data = 'get_language_eng')
        keyboard.add(key_eng)
        bot.send_message(message.from_user.id, text='Выбери язык, с которого переводить', reply_markup=keyboard)
       
        bot.register_next_step_handler(message, get_word_for_translation)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start чтобы начать использовать бот')


def get_word_for_translation(message):
    if message.text == '/start':
        keyboard = types.InlineKeyboardMarkup()
        key_rus = types.InlineKeyboardButton(text='Русский', callback_data = 'get_language_rus')
        keyboard.add(key_rus)
        key_eng = types.InlineKeyboardButton(text='English', callback_data = 'get_language_eng')
        keyboard.add(key_eng)
        
        bot.send_message(message.from_user.id, text='Выбери язык, с которого переводить', reply_markup=keyboard) 
    else:
        bot.send_message(message.from_user.id, translate(message.text))
    bot.register_next_step_handler(message, get_word_for_translation)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global language_from
    global language_to
    if call.data[:12] == 'get_language':
        language_from = call.data[13:16]

        keyboard = types.InlineKeyboardMarkup()
        key_rus = types.InlineKeyboardButton(text='Русский', callback_data = 'translate_rus')
        keyboard.add(key_rus)
        key_eng = types.InlineKeyboardButton(text='English', callback_data = 'translate_eng')
        keyboard.add(key_eng)
    
        bot.send_message(call.message.chat.id, text='Выбери язык, на который переводить', reply_markup=keyboard)
    elif call.data[:9] == 'translate':
        language_to = call.data[10:13]
        bot.send_message(call.message.chat.id, 'Класс! Теперь можешь маленькими буквами по одному писать слова, перевод котоырх хочешь узнать')

bot.polling(none_stop = True, interval = 0)
