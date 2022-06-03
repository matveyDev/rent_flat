from django.urls import path
from .apiviews import ReviewListAPIView, ReviewRetrieveUpdateAPIView, \
    ReviewDestroyAPIView, ReviewCreateAPIView, FlatListAPIView, FlatRetrieveAPIView, \
    ReservationCreateAPIView, ReservationDestroyAPIView, ReservationRetrieveUpdateAPIView

urlpatterns = [
    path('flats/', FlatListAPIView.as_view(), name='api_flat_list'),
    path('flats/<int:id>/', FlatRetrieveAPIView.as_view(), name='api_flat_detail'),
    path('reviews/', ReviewListAPIView.as_view(), name='api_review_list'),
    path('reviews/update/<int:id>/', ReviewRetrieveUpdateAPIView.as_view(), name='api_review_update'),
    path('reviews/delete/<int:id>/', ReviewDestroyAPIView.as_view(), name='api_review_delete'),
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='api_review_create'),
    path('reservations/update/<int:id>/', ReservationRetrieveUpdateAPIView.as_view(), name='api_reservation_update'),
    path('reservations/delete/<int:id>/', ReservationDestroyAPIView.as_view(), name='api_reservation_delete'),
    path('reservations/create/', ReservationCreateAPIView.as_view(), name='api_reservation_create'),
]
