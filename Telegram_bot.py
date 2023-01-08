from random import *
from telebot import types
import telebot


bot = telebot.TeleBot('TOKEN')


num1 = ''
num2 = ''
flag = 1
candy = 117


def game_conditions():
    """Условия игры"""
    return 'Условие игры: На столе лежит 117 конфета. Играют два игрока делая ход друг после друга.\
        \nПервый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет.\
        \nВсе конфеты оппонента достаются сделавшему последний ход.'


def choice_first(user1, user2):
    """Выбират кто первый ходит"""
    num2 = [user1, user2]
    num1 = choice(num2)
    num2.remove(num1)
    return str(num1), str(num2)


def winner(flag, num1, num2):
    """Определение победителя"""
    if num1 == 'я':
        if flag == 2:
            return f'Победил {num1}'
        else:
            return f'{num2.upper()} победил 👍'
    else:
        if flag == 2:
            return f'Победил  {num2}'
        else:
            return f'{num1.upper()} победил 👍'


@bot.message_handler(commands=['start'])
def start_messages(message):
    bot.send_message(message.from_user.id,
                     'Привет я Brick  хочу с тобой сыграть в игру! Чтобы начать напиши мне привет!')


@bot.message_handler(func=lambda message: message.text.lower() == "привет")
def hi_messages(message):
    bot.send_message(message.from_user.id,
                     'Привет ✌️ , пердлагаю сыграть в игру!')
    bot.send_message(message.from_user.id, game_conditions())
    bot.send_message(message.from_user.id,
                     'Xочешь сыграть со мной в конфетки? да/нет')


@bot.message_handler(func=lambda message: message.text.lower() == "нет")
def bye_messages(message):
    bot.send_message(message.from_user.id, f"👌")
    bot.send_message(message.from_user.id,
                     f"Заxочешь сыграть напиши мне ДА или /start")


@bot.message_handler(func=lambda message: message.text.lower() == "да")
def choce_first_user(message):
    global num1, num2, flag, candy
    bot.send_message(message.from_user.id, 'Начинаем жеребьевку. Удачи!')
    num1, num2 = choice_first('я', 'ты')
    if num1 == 'я':
        bot.send_message(message.from_user.id,
                         f'Первым буду ходить {num1}')
        b = randint(1, 29)
        candy -= b
        bot.send_message(message.from_user.id,
                         f'Я беру со стола {b} конфет.\
                            \nНа столе {candy} конфет.')
        bot.send_message(message.from_user.id, 'Сколько возьмешь?')
    else:
        bot.send_message(message.from_user.id,
                         f'Первым будешь ходить {num1}')
        bot.send_message(message.from_user.id,
                         f'На столе {candy} конфет.\nCколько возьмешь?')


@bot.message_handler(func=lambda message: True)
def game(message):
    if int(message.text) > 0 and int(message.text) < 29:
        global candy, flag
        global num1, num2

        if candy > 28:
            candy -= int(message.text)
            bot.send_message(message.from_user.id,
                             f'На cтоле {candy} конфет!')
            flag = 2
            if candy > 28:
                a = randint(1, 29)
                candy -= a
                bot.send_message(message.from_user.id,
                                 f'Я беру со стола {a} конфет.\
                                    \nНа cтоле {candy} конфет!')
                flag = 1
                if candy > 28:
                    bot.send_message(message.from_user.id,
                                     'Сколько ты возьмешь?')

        if candy <= 28:
            bot.send_message(message.from_user.id, winner(flag, num1, num2))
            candy = 117
            bot.send_message(message.from_user.id, "Повторим? да/нет")
    else:
        bot.send_message(message.from_user.id,
                         'Конфет можно взять от 1 до 28! Сколько возьмешь?')


bot.infinity_polling()
