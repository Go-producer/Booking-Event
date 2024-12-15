from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Event
from django.contrib.auth import logout
from django.contrib import messages
import logging
from django.contrib.auth.decorators import user_passes_test
from .models import User
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Хэшируем пароль
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking_app/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = None
            if '@' in username_or_email:
                user = authenticate(request, email=username_or_email, password=password)
            else:
                user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_admin or user.is_staff:  # Если пользователь администратор
                        return redirect('/admin/')  # Перенаправляем в админ-панель
                    return redirect('profile')
                else:
                    form.add_error(None, "Ваш аккаунт отключен.")
            else:
                form.add_error(None, "Неправильный email/логин или пароль.")
    else:
        form = LoginForm()
    return render(request, 'booking_app/login.html', {'form': form})



@login_required
def profile_view(request):
    # Получаем мероприятия, на которые зарегистрирован пользователь
    registered_events = request.user.registered_events.all()

    # Вы можете также добавить посещенные мероприятия, если есть поле для этого
    context = {
        'registered_events': registered_events,
        # Если нужно обработать "посещенные" мероприятия, добавьте здесь логику
    }
    return render(request, 'booking_app/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа после выхода

def home_view(request):
    return render(request, 'booking_app/home.html')  # Шаблон для главной страницы

#Пример регистрации на мероприятия(Позже сделать нормальный)
@login_required
def register_to_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.registered_users.add(request.user)
    return redirect('profile')


#Все мероприятия
def events_list(request):
    events = Event.objects.all()  # Получаем все мероприятия
    return render(request, 'booking_app/events_list.html', {'events': events})

#Контакты
def contact_view(request):
    return render(request, 'booking_app/contact.html')

# Проверка на роль администратора
def admin_check(user):
    return user.is_admin or user.is_staff

@user_passes_test(admin_check)  # Только для администраторов
def users_list(request):
    users = User.objects.all()
    return render(request, 'booking_app/users_list.html', {'users': users})