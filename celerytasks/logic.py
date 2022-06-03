from arenda.models import Reservation
from flat.models import Flat
from django.core.mail import send_mail
from .config import SITE_URL

def set_field_empty(flat_ids):
    for pk in flat_ids:
        flat = Flat.objects.get(pk=pk)

        if flat.reviews.count() == 0:
            # Если нет бронирований
            flat.empty = True
            flat.save()
        else:
            pass

def delete_reservations(reserv_ids):
    # Удаляем все бронирования, которые закончились
    for pk in reserv_ids:
        reservation = Reservation.objects.get(pk=pk)
        reservation.delete()

def send(flats, users, flat_ids):
    # Для каждой квартиры каждому пользователю отправим письмо,
    # id - id квартиры для передачи правильной ссылки
    for flat, id in zip(flats, flat_ids):
        for user in users:
            send_mail(
                'Освободилась квартира!',
                f'Квартира по адресу: {flat}. Ссылка: {SITE_URL}{id}/',
                'noreplyarenda@gmail.com',
                [user.email,],
                fail_silently=False,
            )