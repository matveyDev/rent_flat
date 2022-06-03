from django.contrib import admin
from .models import Reservation
from django import forms

class ReservationAdminForm(forms.ModelForm):
  class Meta:
    model = Reservation
    fields = '__all__'


@admin.register(Reservation)
class FlatAdmin(admin.ModelAdmin):
    form = ReservationAdminForm
    list_display = ('flat', 'client', 'arenda_date_start', 'arenda_date_finish')
    search_fields = ('arenda_date_start', 'arenda_date_finish', 'flat', 'client')
    fields = ('flat', 'client', 'arenda_date_start', 'arenda_date_finish')