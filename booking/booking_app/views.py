from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import Event
from django.contrib.auth import logout
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
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

            # Проверка: является ли ввод email или логином
            user = None
            if '@' in username_or_email:  # Если пользователь ввел email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            else:  # Если пользователь ввел логин
                user = authenticate(request, username=username_or_email, password=password)

            # Аутентификация и вход
            if user is not None:
                login(request, user)
                return redirect('profile')  # Перенаправление на страницу пользователя
            else:
                messages.error(request, "Неправильный email/логин или пароль.")
    else:
        form = LoginForm()

    return render(request, 'booking_app/login.html', {'form': form})



@login_required
def profile_view(request):
    # Пример данных о мероприятиях
    registered_events = Event.objects.filter(registered_users=request.user)
    visited_events = Event.objects.filter(visited_users=request.user)

    context = {
        'registered_events': registered_events,
        'visited_events': visited_events,
    }
    return render(request, 'booking_app/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа после выхода

def home_view(request):
    return render(request, 'booking_app/home.html')  # Шаблон для главной страницы