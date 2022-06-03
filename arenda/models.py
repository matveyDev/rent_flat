from datetime import datetime
from django.db import models
from flat.models import Flat
from django.contrib.auth import get_user_model


#Бронирование
class Reservation(models.Model):
    flat = models.ForeignKey(Flat, verbose_name='Квартира', related_name='reservations', on_delete=models.CASCADE)
    client = models.ForeignKey(get_user_model(), verbose_name='Клиент', null=True, related_name='client', on_delete=models.CASCADE)
    arenda_date_start = models.DateTimeField(verbose_name='Дата начала')
    arenda_date_finish = models.DateTimeField(verbose_name='Дата окончания')

    def __str__(self):
        return str(self.arenda_date_start)[0:-9] + ' - ' + str(self.arenda_date_finish)[0:-9]
        
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['arenda_date_start']