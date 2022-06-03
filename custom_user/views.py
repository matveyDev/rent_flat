from django.shortcuts import redirect, render
from django.views.generic import DetailView, UpdateView
from arenda.models import Reservation
from flat.models import Review
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


class ProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'templates/custom_user/profile.html'
    context_object_name = 'user'
    fields = ['first_name', 'last_name', 'phone']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.filter(client_id=self.kwargs['pk'])
        context['reviews'] = Review.objects.filter(author_id=self.kwargs['pk'])
        context['user_pk'] = self.object.pk
        return context


class ProfileUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'templates/custom_user/update_profile.html'
    fields = ['first_name', 'last_name', 'phone']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = Reservation.objects.filter(client_id=self.kwargs['pk'])
        context['reviews'] = Review.objects.filter(author_id=self.kwargs['pk'])
        context['user_pk'] = self.object.pk
        return context

    def get_success_url(self):
        return reverse_lazy('user_update', kwargs={'pk': self.object.pk})