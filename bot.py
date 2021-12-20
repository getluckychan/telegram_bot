# -*- coding: utf-8 -*-
import telebot
from pprint import pprint
from telebot import types
import os


PORT = int(os.environ.get('PORT', 5000))
bot = telebot.TeleBot("token")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    pprint(vars(message))
    bot.send_message('-584475199', "Кто-то запустил бота. Ник ниже")
    bot.send_message('-584475199', message.chat.username)
    bot.reply_to(message,
                 "Привіт. Я - бот, що допоможе вам. Натисніть /help щоб дізнатися про послуги, що ми можемо надати.")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,
                 text="Графік роботи:\nбудні дні 9:00-19:00\nсубота 10:00-17:00\nнеділя - вихідний\nНатисніть на "
                      "/location щоб дізнатися де ми знаходимося")
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Фото на документи')
    itembtn2 = types.KeyboardButton('Роздрук фото та текстів')
    itembtn10 = types.KeyboardButton('Ксерокопія')
    itembtn3 = types.KeyboardButton('Назад')
    markup1.add(itembtn1, itembtn2, itembtn3, itembtn10)
    bot.reply_to(message, "Виберіть необхідну послугу:", reply_markup=markup1)


@bot.message_handler(commands=['Роздрук_фото_та_текстів'], content_types=['text'])
def print(message):
    bot.reply_to(message, "Відправте мені файл чи фото, що ви бажаєте роздрукувати.")  # печать всего


@bot.message_handler(content_types=['document'])  # если отправят документ
def document(message):
    pprint(vars(message))
    bot.send_document('-584475199', message.document.file_id)
    bot.send_message('-584475199', message.chat.username)
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    itembtn5 = types.KeyboardButton('Відправити свій контакт', request_contact=True)
    itembtn3 = types.KeyboardButton('Назад')
    markup2.add(itembtn5, itembtn3)
    bot.reply_to(message,
                 "Надішліть нам наш контакт по кнопці знизу і з вами зв'яжуться найближчим часом для уточнення інформації",
                 reply_markup=markup2)


def what(message):
    pprint(vars(message))
    bot.send_message('-584475199', message.chat.username)
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    itembtn5 = types.KeyboardButton('Відправити свій контакт', request_contact=True)
    itembtn3 = types.KeyboardButton('Назад')
    markup2.add(itembtn5, itembtn3)
    bot.reply_to(message,
                 "Надішліть нам наш контакт по кнопці знизу і з вами зв'яжуться найближчим часом для уточнення інформації",
                 reply_markup=markup2)


@bot.message_handler(commands=['location'])  # робочая локация
def location(message):
    bot.reply_to(message, "Ми знаходимося за адресою м. Житомир, вул. Шевченко 16")
    bot.send_location(message.chat.id, 50.247903, 28.677650)


@bot.message_handler(content_types=["text"])  # спрашивает доки
def doc_photo(message):
    if message.chat.type == 'private':
        if message.text == 'Фото на документи':
            bot.reply_to(message,
                         "Фотографуємо та друкуємо фото на документи. Також ви можете завітати до нас по адресі в /location")
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Контакт", url="https://t.me/sergey_kriuchikhin")
            keyboard.add(url_button)
            bot.send_message(message.chat.id, "Натисніть на кнопку нижче щоб зв'язатися з людиною.",
                             reply_markup=keyboard)
        elif message.text == 'Ксерокопія':
            bot.reply_to(message,
                         "Ксерокопію робимо протягом всього робочого часу. Знайти нас можливо за допомогою /location")
        elif message.text == 'Роздрук фото та текстів':
            bot.reply_to(message, "Відправте мені файл чи фото, що ви бажаєте роздрукувати.")
        elif message.text == 'Назад':
            send_help(message)
        else:
            bot.send_message('-584475199', message.text)
            what(message)


@bot.message_handler(content_types=["photo"])  # если отправят фотки
def photo_print(message):
    bot.send_photo('-584475199', message.photo[-1].file_id)
    bot.send_message(message.chat.id, 'Напишіть якого розміру необхідне фото')
    bot.send_message('-584475199', message.chat.username)


@bot.message_handler(content_types=["text"])
def get_messages(m):
    pprint(vars(m))
    bot.send_message('-584475199', m.text)
    bot.send_message('-584475199', m.chat.username)
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    itembtn5 = types.KeyboardButton('Відправити свій контакт', request_contact=True)
    markup2.add(itembtn5)
    bot.reply_to(m,
                 "Надішліть нам наш контакт по кнопці знизу і з вами зв'яжуться найближчим часом для уточнення інформації",
                 reply_markup=markup2)


@bot.message_handler(content_types=['contact'])  # пересылает контакт
def contact(message):
    pprint(vars(message))
    bot.send_message('-584475199', message.contact.first_name)
    bot.send_message('-584475199', message.contact.phone_number)
    bot.send_message('-584475199', message.chat.username)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
