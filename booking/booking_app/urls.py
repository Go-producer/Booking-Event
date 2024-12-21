from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.login_view, name='login'),      # Авторизация
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('events/', views.events_list, name='events_list'),
    path('contact/', views.contact_view, name='contact'),
    path('users/', views.users_list, name='users_list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
