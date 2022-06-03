from django import template
import datetime

date_now = datetime.timezone(datetime.timedelta(hours=3))
current_date_now = datetime.datetime.now(date_now)

register = template.Library()

@register.filter()
def over_today(arenda_date_finish):
    correct_format_arenda_date_finish = datetime.datetime.strptime(str(arenda_date_finish), '%Y-%m-%d %H:%M:%S%z')
    return current_date_now <= correct_format_arenda_date_finish

@register.filter()
def count_true_reservations(reservations):
    #counter для подсчета дат бронирования, не превышающих сегодняшнюю дату
    counter = 0
    #Для каждого бронирования: преобразовываем в правильный формат 
    for reserv in reservations:
        correct_format_arenda_date_finish = datetime.datetime.strptime(str(reserv.arenda_date_finish), '%Y-%m-%d %H:%M:%S%z')
        #Если Сегодняшняя дата меньше, чем конечная дата бронирвоания, добавить +1 в counter
        #Пояснение: Если бронирование актуально, добавим +1 в counter
        if current_date_now <= correct_format_arenda_date_finish:
            counter += 1
        else:
            pass
    return counter