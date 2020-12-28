from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('change_profile/', views.UserUpdateView.as_view(), name = 'change_profile'),
    path('profile/', views.profile, name='profile'),
]
