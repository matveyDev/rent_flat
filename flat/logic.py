from arenda.models import Reservation
from .models import Review
from flat.models import Flat
import datetime

def set_field_empty(pk):
    flat = Flat.objects.get(pk=pk)
    flat.empty = False
    flat.save()

def create_reservation(flat, client, arenda_date_start, arenda_date_finish):
    Reservation.objects.create(
        flat=flat,
        client=client,
        arenda_date_start=arenda_date_start,
        arenda_date_finish=arenda_date_finish,
    )

def create_review(author, flat, rating, text):
    Review.objects.create(
        author=author,
        flat=flat,
        rating=rating,
        text=text
    )

#Сегодняшняя дата
date_now = datetime.timezone(datetime.timedelta(hours=3))
current_date_now = datetime.datetime.now(date_now)

def correct_format(arenda_date):
    #Преобразуем в корректный формат
    correct_format_arenda_date = datetime.datetime.strptime(str(arenda_date), '%Y-%m-%d %H:%M:%S%z')

    return correct_format_arenda_date


def date_finish_over_start(arenda_date_start, arenda_date_finish):
    #Делаем корректные форматы дат для сравнения
    correct_format_arenda_date_start = correct_format(arenda_date_start)
    correct_format_arenda_date_finish = correct_format(arenda_date_finish)

    #True, если дата выезда позднее даты заезда
    return correct_format_arenda_date_start < correct_format_arenda_date_finish

def not_past_date(arenda_date_start):
    #Преобразуем в корректный формат
    correct_format_arenda_date_start = correct_format(arenda_date_start)

    #True, если дата и время заезда позднее, чем сейчас
    return correct_format_arenda_date_start >= current_date_now

# Работу алгоритма см. внизу
def dates_between_arenda(arenda_date_start, arenda_date_finish, pk):
    days_arenda_finish = [current_date_now, ]
    reservs_finish_date = Reservation.objects.filter(flat_id=pk, arenda_date_start__gte=current_date_now).values_list('arenda_date_finish')
    for reserv in reservs_finish_date:
        # reserv - это массив, распакуем его
        for date in reserv:
            days_arenda_finish.append(date)

    days_arenda_start = []
    reservs_start_date = Reservation.objects.filter(flat_id=pk, arenda_date_start__gte=current_date_now).values_list('arenda_date_start')
    for reserv in reservs_start_date:
        # reserv - это массив, распакуем его
        for date in reserv:
            days_arenda_start.append(date)

    infinity_date = datetime.datetime(3000, 5, 29, 13, 56, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)))
    days_arenda_start.append((infinity_date))
    
    correct_arenda_date_start = correct_format(arenda_date_start)
    correct_arenda_date_finish = correct_format(arenda_date_finish)

    bool_list_start_days = []
    for day in days_arenda_finish:
        if correct_arenda_date_start >= day:
            bool_list_start_days.append(True)
        else:
            bool_list_start_days.append(False)

    bool_list_finish_days = []
    for day in days_arenda_start:
        if correct_arenda_date_finish <= day:
            bool_list_finish_days.append(True)
        else:
            bool_list_finish_days.append(False)
    
    bool_correct = []
    for day_start, day_finish in zip(bool_list_start_days, bool_list_finish_days):
        if day_start and day_finish:
            bool_correct.append(True)
        else:
            bool_correct.append(False)

    return True in bool_correct


def validate_date(arenda_date_start, arenda_date_finish, pk):
    #Дата выезда позднее даты заселения (True/False)
    finish_over_start = date_finish_over_start(arenda_date_start, arenda_date_finish)
    #Дата заезда не меньше сегодняшней даты (True/False)
    not_past_arenda_date = not_past_date(arenda_date_start)
    #Дата и время заезда и выезда не пересекаются с другими бронированиями (True/False)
    current_dates = dates_between_arenda(arenda_date_start, arenda_date_finish, pk)

    #True, если данные прошли всю валидацию
    return finish_over_start and not_past_arenda_date and current_dates




# Алгоритм функции dates_between_arenda() :
# Достаем все даты заездов и выездов из квартиры.
# 
# Сам алгоритм: Дата заезда клиента >= любой из дат выездов,
#               Дата выезда <= любой из дат ЗАЕЗДА СЛЕДУЮЩЕГО бронирвоания.
#
# Поэтому мы добавляем в начало листа days_arenda_finish сегодняшнее число,
# А в конец листа days_arenda_start добавляем дату 3000 года, тем самым
# проверка даты заезда будет уже сравниваться со следующим бронирвоанием
# 
# Попутно я преобразую даты в верные для сравнения форматы.
# 
# Далее у нас есть bool_list_start_days и bool_list_finish_days
# В bool_list_start_days мы сравниваем ДАТУ заезда с датами выезда
# В bool_list_finish_days мы сравниваем ДАТУ выезда с датами заезда (уже следующего броинрвоания)
# Добавляем True, если удовлетворяет условию
# 
# Циклом в bool_current добавляем True, если в однономерном индексе 
# bool_list_start_days и bool_list_finish_days содержится True, иначе False
# (Например)
# Под индексом 0 в bool_list_start_days находится True, и в bool_list_finish_days
# под индексом 0 находится True, то запишем в bool_correct - True
# 
# Возвращаем True, если в bool_correct есть хоть одно True, иначе False