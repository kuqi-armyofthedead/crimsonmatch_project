from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('like/<int:user_id>/', views.like_user, name='like_user'),
    path('matches/', views.matches, name='matches'),
]
