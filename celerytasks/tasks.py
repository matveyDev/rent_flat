from celery import shared_task
from django.contrib.auth import get_user_model
from arenda.models import Reservation
from flat.models import Flat
from .logic import delete_reservations, send, set_field_empty

import datetime

@shared_task
def send_notifications():
    # Дата СЕЙЧАС
    date_now = datetime.timezone(datetime.timedelta(hours=3))
    current_date_now = datetime.datetime.now(date_now)

    # Получаем всех юзеров
    user_model = get_user_model()
    users = user_model.objects.all()

    # Получаем все бронирвоания
    reservations = Reservation.objects.all()
    # Список всех id бронирований
    reserv_ids = []

    # Список для всех адресов квартир
    flats = []
    # Переменная для получения id квартиры
    flat_num = ''
    # Сисок для добавления всех id 
    flat_ids = []
    # Переменная для поулчения адреса квартиры
    flat_address = ''

    # Для каждого бронирвоания:
    for reserv in reservations:
        correct_format_arenda_date_finish = datetime.datetime.strptime(str(reserv.arenda_date_finish), '%Y-%m-%d %H:%M:%S%z')

        # Если бронирование устарело
        if current_date_now >= correct_format_arenda_date_finish:

            # Получаем id квартиры
            flat_num = reserv.flat_id
            # Запишем в список id квартиры
            flat_ids.append(flat_num)
            # Получаем адресс квартиры
            flat_address = Flat.objects.get(pk=flat_num).address
            # Запишем в список адресс квартиры
            flats.append(flat_address)
            # Запишем в список id бронирования для дальнейшего удаления
            reserv_ids.append(reserv.id)
        else:
            pass
    
    if flats:
        send(flats, users, flat_ids)
    else:
        return

    if reserv_ids:
        delete_reservations(reserv_ids)
        set_field_empty(flat_ids)
    else:
        pass