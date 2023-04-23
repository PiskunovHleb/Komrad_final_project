import sqlite3
import telebot
import random
import ch_1

from telebot import types

bot = telebot.TeleBot("6276907923:AAE1PTsXImlem9mfBwqkpRVmNBeOAa2zM14")
Pep_Char = ""


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Подбор")
    item2 = types.KeyboardButton("💬 Заполнить анкету")
    item3 = types.KeyboardButton("▶ Музыка для игры")
    item4 = types.KeyboardButton("📋 Моя анкета")

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                     "Этот бот создан для поиска товарищей по игре и т.д.\n"
                     "Заполните анкету, чтобы вам могли написать".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def keyBoard(message):
    global zxc
    global rez
    Pep_Char = ""
    user_id = message.from_user.username
    if message.chat.type == 'private':
        if message.text == '🎲 Подбор':
            try:
                con = sqlite3.connect("static/botDB.db")
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("👍", callback_data='like')
                item2 = types.InlineKeyboardButton("👎", callback_data='dislike')
                markup.add(item1, item2)
                cur = con.cursor()
                result = cur.execute("""SELECT user_id, about FROM alb""").fetchall()
                kolvo = (len(result))
                rez = result[(random.randint(0, kolvo - 1))]
                bot.send_message(message.chat.id, f"{(rez[1])[0:-7]} @{rez[0]}", reply_markup=markup)
            except Exception as e:
                print(repr(e))
        elif message.text == '💬 Заполнить анкету':
            zxc = True
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Отмена", callback_data='cancel')
            markup.add(item1)
            bot.send_message(message.chat.id, 'Как заполнить анкету:\n'
                                              'Укажите свое имя, возраст, любимые игры/занятия, удобное время\n'
                                              'Весь текст должен быть в 1 сообщение\n'
                                              'Также необходимо в конце ввести кодовое слово: Комрад\n'
                                              'В случае отказа нажмите Отмена\n'
                                              'Для перезаполнения анкеты используйте функцию еще раз',
                             reply_markup=markup)
        if "Комрад" in message.text or "комрад" in message.text or "КОМРАД" in message.text:
            if zxc:
                Pep_Char = message.text
                ch_1.db_table_completion(user_id=f"{message.from_user.username}", about=f"{message.text}")
                bot.send_message(message.chat.id, f'Вы заполнили анкету')
                zxc = False
                print(Pep_Char, message.from_user.username)
        if message.text == '▶ Музыка для игры':
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text='Фонк', url='https://youtu.be/k9RU4uW0kSY')
            btn2 = types.InlineKeyboardButton(text='Спокойная музыка', url='https://youtu.be/TiK_u2-SQDQ')
            btn3 = types.InlineKeyboardButton(text='Для дотеров', url='https://youtu.be/CP1K9MW7cfg')
            btn4 = types.InlineKeyboardButton(text='Майнкрафт музыка', url='https://youtu.be/oKIZfBRO8ug')
            btn5 = types.InlineKeyboardButton(text='?', url='https://youtu.be/dQw4w9WgXcQ')
            markup.add(btn1, btn2, btn3, btn4, btn5)
            bot.send_message(message.from_user.id, "Музыка на любой вкус для комфортной игры", reply_markup=markup)
        if message.text == '📋 Моя анкета':
            bot.send_message(message.from_user.id,
                             f'Ваша анкета:\n{ch_1.get_about(user_id=message.from_user.username)}')
            bot.send_message(message.from_user.id,
                             f'Количество лайков: {ch_1.get_like(user_id=message.from_user.username)}')
            bot.send_message(message.from_user.id,
                             f'Количество дизлайков:{ch_1.get_dislike(user_id=message.from_user.username)}')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global zxc
    try:
        if call.message:
            if call.data == 'cancel':
                zxc = False
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Заполнение анкеты отменено",
                                      reply_markup=None)
            if call.data == 'like':
                print(rez[0])
                ch_1.set_like(user_id=rez[0])
                x = ch_1.get_like(user_id=rez[0])
                y = ch_1.get_dislike(user_id=rez[0])
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"{(rez[1])[0:-7]} @{rez[0]}\n 👍 - {x}, 👎 - {y}",
                                      reply_markup=None)
            elif call.data == 'dislike':
                ch_1.set_dislike(user_id=rez[0])
                x = ch_1.get_like(user_id=rez[0])
                y = ch_1.get_dislike(user_id=rez[0])
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"{(rez[1])[0:-7]} @{rez[0]}\n 👍 - {x}, 👎 - {y}",
                                      reply_markup=None)
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True, interval=0)
