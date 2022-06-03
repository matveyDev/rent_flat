from django.urls import path
from .views import user_logout
from .views import ListFlatView, DetailFlatView, ContactView, DeleteReviewView, UpdateReviewView, CreateReservationView, ReviewListView



urlpatterns = [
    path('', ListFlatView.as_view(), name='home'),
    path('user_logout/', user_logout, name='logout'),
    path('contact_us/', ContactView.as_view(), name='contact_us'),
    path('<int:pk>/', DetailFlatView.as_view(), name='flat_detail'),
    path('reviews/delete/<int:pk>/', DeleteReviewView.as_view(), name='delete_review'),
    path('reviews/update/<int:pk>/', UpdateReviewView.as_view(), name='update_review'),
    path('reservation/<int:pk>/', CreateReservationView.as_view(), name='create_reservation'),
    path('reviews/', ReviewListView.as_view(), name='reviews_list'),
    
]
