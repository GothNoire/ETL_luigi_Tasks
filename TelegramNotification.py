import telebot
import traceback
from luigi import Task


def send_err_tlg_notif(task: Task, exception: Exception):
    chat_id = ['554900514','962581764','444655587','1327219370','404163509']
    message_text = f'Сломався таск:{task.__class__.__name__}' + f' Исключение:{exception.__class__.__name__} '+f' Трейс:{traceback.format_exc()}'
    bot = telebot.TeleBot('5078862539:AAFDie49p_T0lbeOzOp0NHda_3u4tMokFZI')
    for rec in chat_id:
        bot.send_message(rec, message_text)

def send_start_tlg_notif(task: Task):
    chat_id = ['554900514','962581764','444655587','1327219370','404163509']
    message_text = f'Запустився таск: {task.__class__.__name__}'
    bot = telebot.TeleBot('5078862539:AAFDie49p_T0lbeOzOp0NHda_3u4tMokFZI')
    for rec in chat_id:
        bot.send_message(rec, message_text)

def send_succes_tlg_notif(task: Task):
    chat_id = ['554900514','962581764','444655587','1327219370','404163509']
    message_text = f'Таска {task.__class__.__name__} выполнилась успешно!'
    bot = telebot.TeleBot('5078862539:AAFDie49p_T0lbeOzOp0NHda_3u4tMokFZI')
    for rec in chat_id:
        bot.send_message(rec, message_text)