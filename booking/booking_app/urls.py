from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.login_view, name='login'),      # Авторизация
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('events/', views.events_list, name='events_list'),
    path('contact/', views.contact_view, name='contact'),
]
