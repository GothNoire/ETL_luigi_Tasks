
import DownloadTaxiModule
import telebot
import traceback
from luigi import Task
import DownloadTaxiModule
import glob

chat_id = ['554900514','962581764','1327219370','404163509']
bot = telebot.TeleBot('5078862539:AAFDie49p_T0lbeOzOp0NHda_3u4tMokFZI')

def send_notif (message_text: str):
    for rec in chat_id:
        bot.send_message(rec, message_text)

def set_err_tlg_notif(task: Task, exception: Exception):
    message_text = f'Сломався таск:{task.__class__.__name__}' + f' Исключение:{exception.__class__.__name__} '+f' Трейс:{traceback.format_exc()}'
    send_notif (message_text)

def set_start_tlg_notif(task: Task):
    message_text = f'Запустився таск: {task.__class__.__name__}'
    send_notif(message_text)

def set_succes_tlg_notif(task: Task):
    message_text = f'Таска {task.__class__.__name__} выполнилась успешно! '
    send_notif (message_text)
    if task.__class__.__name__ == 'YellowTaxiDateRangeTask':
        for rec in chat_id:
            for file in glob.glob('taxi_file/aggr_yellow_tripdata_*.csv'):
                bot.send_document(rec, open(file, 'rb'))
