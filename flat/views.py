from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin, FormView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.http import HttpResponse

from .models import Flat, Review
from arenda.models import Reservation
from .forms import ReviewForm, ContactForm, ReservationForm
from django.contrib import messages
from django.db.models import Avg, Func
import datetime
from .logic import validate_date, create_review, create_reservation, set_field_empty
from .service import send_contact

date_now = datetime.timezone(datetime.timedelta(hours=3))


def user_logout(request):
    logout(request)
    return redirect('/')


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'templates/flat/contact_us.html'

    def post(self, request):
        form = ContactForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data
            message=clean_form['text']
            email=clean_form['email']

            if clean_form['phone']:
                phone = clean_form['phone']
            else:
                phone = '(номер не указан)'
            author = request.user

            send_contact(email, author, phone, message)

            messages.success(request, 'Успешно отправлено!')

        else:
            form = ContactForm()
            
        return redirect('contact_us')


class ListFlatView(ListView):
    model = Flat          
    template_name = 'templates/flat/home_list_flats.html'
    context_object_name = 'flats'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'


class DetailFlatView(FormMixin, DetailView):
    model = Flat
    template_name = 'templates/flat/detail_view.html'
    context_object_name = 'flat'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews_by_id = Review.objects.filter(flat_id=self.kwargs['pk'])
        reservs_by_id = Reservation.objects.filter(flat_id=self.kwargs['pk'])

        context['reviews'] = reviews_by_id
        context['average_rating'] = reviews_by_id.aggregate(avg=Round(Avg('rating')))
        context['reservations'] = reservs_by_id.exclude(arenda_date_finish__lt=datetime.datetime.today())
        return context

    def post(self, request, pk):
        form = ReviewForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data

            author = request.user
            flat = get_object_or_404(Flat, pk=pk)
            rating = clean_form['rating']
            text = clean_form['text']
            create_review(author, flat, rating, text)

        else:
            form = ReviewForm()

        return redirect('flat_detail', pk=pk)


class DeleteReviewView(DeleteView):
    model = Review
    template_name = 'templates/flat/delete_review.html'
    context_object_name = 'reviews_for_delete'

    def get_success_url(self):
        return reverse_lazy('flat_detail', kwargs={'pk': self.object.flat_id})

    def post(self, request, *args, **kwargs):
        if HttpResponse.status_code == 200:
            messages.success(request, 'Успешно удалено!')
        else:
            messages.error(request, 'Произошла ошибка!')

        return super().post(request, *args, **kwargs)


class UpdateReviewView(UpdateView):
    model = Review
    template_name = 'templates/flat/update_review.html'
    context_object_name = 'reviews_for_update'
    form_class = ReviewForm

    def get_success_url(self):
        return reverse_lazy('flat_detail', kwargs={'pk': self.object.flat_id})

    def post(self, request, *args, **kwargs):
        if HttpResponse.status_code == 200:
            messages.success(request, 'Успешно обновлено!')
        else:
            messages.error(request, 'Произошла ошибка!')

        return super().post(request, *args, **kwargs)


class ReviewListView(ListView):
    model = Review
    template_name = 'templates/flat/reviews_list.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['average_rating'] = Review.objects.aggregate(avg=Round(Avg('rating')))
        return context
    

class CreateReservationView(FormMixin, DetailView):
    model = Flat
    context_object_name = 'flat'
    template_name = 'templates/flat/reservation.html'
    form_class = ReservationForm


    def post(self, request, pk):
        form = ReservationForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data
            arenda_date_start = clean_form['arenda_date_start']
            arenda_date_finish = clean_form['arenda_date_finish']
            client = request.user
            flat = get_object_or_404(Flat, pk=pk)

            if validate_date(arenda_date_start, arenda_date_finish, flat):
                create_reservation(flat, client, arenda_date_start, arenda_date_finish)
                set_field_empty(pk=pk)
                messages.success(request, 'Успешно забронировано!')
            else:
                messages.error(request, 'Некорректно введены даты')

        else:
            form = ReservationForm()

        
        return redirect('create_reservation', pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews_by_id = Review.objects.filter(flat_id=self.kwargs['pk'])
        reservs_by_id = Reservation.objects.filter(flat_id=self.kwargs['pk'])

        context['reviews'] = reviews_by_id
        context['average_rating'] = reviews_by_id.aggregate(avg=Round(Avg('rating')))
        context['reservations'] = reservs_by_id.exclude(arenda_date_finish__lt=datetime.datetime.today())
        return context