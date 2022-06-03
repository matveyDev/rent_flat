from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='user_profile'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='user_update'),
]
