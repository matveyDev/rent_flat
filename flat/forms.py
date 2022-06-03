from django.forms import widgets
from arenda.models import Reservation
from django import forms
from .models import Review

REVIEW_CHOICES = [('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5')]


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
            'rating': forms.RadioSelect(
                choices=REVIEW_CHOICES
            ),
        }


class ContactForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=11, required=False, label='Телефон',
    )
    text = forms.CharField(max_length=400, required=True, label='Обращение',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )


class ReservationForm(forms.Form):
    arenda_date_start = forms.DateTimeField(label='Дата заезда', required=True,
        widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M',
        attrs={
            'class': 'flatpickr',
            'placeholder': 'Выберите дату и время'
            })
    )
    arenda_date_finish = forms.DateTimeField(label='Дата выезда', required=True,
        widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M',
        attrs={
            'class': 'flatpickr',
            'placeholder': 'Выберите дату и время'
        })
    )