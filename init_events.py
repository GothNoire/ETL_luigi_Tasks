from luigi import Task
from luigi.event import Event

from TelegramNotification import send_err_tlg_notif
from TelegramNotification import send_start_tlg_notif
from TelegramNotification import send_succes_tlg_notif


Task.event_handler(Event.FAILURE)(send_err_tlg_notif)
Task.event_handler(Event.START)(send_start_tlg_notif)
Task.event_handler(Event.SUCCESS)(send_succes_tlg_notif)
