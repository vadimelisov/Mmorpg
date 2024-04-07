import datetime
from random import seed, randint

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from members.forms import RegistrationForm, MyActivationCodeForm
from members.models import Profile
from sitecore.settings import DEFAULT_FROM_EMAIL


def generate_code():
    seed()
    return str(randint(10000, 99999))


def sign_up(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user_reg = form.save(commit=False)
                user_reg.is_active = False
                form.save()

                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password = form.cleaned_data.get('password1')
                u_f = User.objects.get(username=username, email=email, is_active=False)

                code = generate_code()

                message = code
                user = authenticate(username=username, password=my_password)
                now = datetime.datetime.now()

                Profile.objects.create(user=u_f, code=code, date=now)

                send_mail(
                    'Код подтверждения',
                    message,
                    DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )

                if user and user.is_active:
                    login(request, user)
                    redirect('/posts/')
                else:
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('http://127.0.0.1:8000/auth/activation/')
            else:
                return render(request, 'members/signup.html', {'form': form})
        else:
            return render(request, 'members/signup.html', {'form': RegistrationForm()})
    else:
        return redirect('/posts/')


def activation(request):
    if request.user.is_authenticated:
        return redirect('/posts/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get('code')
                if Profile.objects.filter(code=code_use):
                    profile = Profile.objects.get(code=code_use)
                else:
                    form.add_error(None, 'Неправильный код')
                    return render(request, 'members/activate.html', {'form': form})
                if not profile.user.is_active:
                    profile.user.is_active = True
                    profile.user.save()

                    user = authenticate(request, username=profile.user.username, password=profile.user.password)
                    if user is not None:
                        login(request, user)

                    profile.delete()
                    return redirect('/auth/login')
                else:
                    form.add_error(None, 'Unknown or disabled account')
                return render(request, 'members/activate.html', {'form': form})
            else:
                form.add_error(None, 'Форма не валидна')
                return render(request, 'members/activate.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'members/activate.html', {'form': form})
