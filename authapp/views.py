from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.db import transaction
from authapp.forms import TravelUserRegisterForm, TravelUserLoginForm, TravelUserEditForm, TravelUserProfileEditForm


# Регистрация пользователя
def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = TravelUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = TravelUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


# Аутентификация пользователя
def login(request):
    title = 'вход'

    login_form = TravelUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    content = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }

    return render(request, 'authapp/login.html', content)


# Завершение сессии
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


# Редактирование данных пользователя и его профиля
@transaction.atomic()
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = TravelUserEditForm(request.POST,
                                       request.FILES, instance=request.user)
        profile_form = TravelUserProfileEditForm(
            request.POST, instance=request.user.traveluserprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = TravelUserEditForm(instance=request.user)
        profile_form = TravelUserProfileEditForm(instance=
                                                 request.user.traveluserprofile)

    content = {'title': title,
               'edit_form': edit_form,
               'profile_form': profile_form}

    return render(request, 'authapp/edit.html', content)
