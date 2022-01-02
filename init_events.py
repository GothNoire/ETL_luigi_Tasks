from luigi import Task
from luigi.event import Event


import TelegramNotification


Task.event_handler(Event.FAILURE)(TelegramNotification.set_err_tlg_notif)
Task.event_handler(Event.START)(TelegramNotification.set_start_tlg_notif)
Task.event_handler(Event.SUCCESS)(TelegramNotification.set_succes_tlg_notif)

