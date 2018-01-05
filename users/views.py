# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404

from sc.forms import UserForm, ProfileForm
from sc.models import Submission
from sc.views import getCreativeByType
from sc_main.settings.common import REG_PASSWORD
from users.models import ScUser


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = ScUser.objects.get(user=user)

    return render(request, 'public/profile.html', {
        'profile': profile,
        'flgMainPage': False,
        'canEdit': request.user == user,
        'date': profile.getDate(),
        'power_karma_color': profile.getPowerKarmaColor(),
        'power_karma_val': profile.getShortPowerKarma(),
        'creative_karma_color': profile.getCreativeKarmaColor(),
        'creative_karma_val': profile.getShortCreativeKarma(),
    })


def user_video(request, username):
    return getCreativeByType(request, 'Видео', Submission.TP_USER_CREATIVE, username)


def user_design(request, username):
    return getCreativeByType(request, 'Дизайн', Submission.TP_USER_CREATIVE, username)


def user_conception(request, username):
    return getCreativeByType(request, 'Концепция', Submission.TP_USER_CREATIVE, username)


def user_story(request, username):
    return getCreativeByType(request, 'Сюжет', Submission.TP_USER_CREATIVE, username)


def user_music(request, username):
    return getCreativeByType(request, 'Музыка', Submission.TP_USER_CREATIVE, username)


def user_invention(request, username):
    return getCreativeByType(request, 'Изобретения', Submission.TP_USER_CREATIVE, username)


def user_creative(request, username):
    return getCreativeByType(request, '', Submission.TP_USER_CREATIVE, username)


@login_required
def edit_profile(request):
    user = ScUser.objects.get(user=request.user)

    if request.method == 'GET':
        profile_form = ProfileForm(instance=user)

    elif request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.update_profile_data()
            profile.save()
            # messages.success(request, "Profile settings saved")
    else:
        raise Http404

    return render(request, 'private/edit_profile.html', {'form': profile_form, 'caption': 'Добавить пост'})


def user_login(request):
    """
    Pretty straighforward user authentication using password and username
    supplied in the POST request.
    """

    if request.user.is_authenticated():
        # messages.warning(request, "You are already logged in.")
        return render(request, 'public/login.html')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return HttpResponseBadRequest()

        user = authenticate(username=username,
                            password=password)

        if user:
            if user.is_active:
                login(request, user)
                redirect_url = request.POST.get('next') or 'frontpage'
                return redirect('/user/' + username + '/')
            else:
                # messages.error("Доступ запрещён")
                return render(request, 'public/login.html',
                              {'login_error': "Аккаунт запрещён"})
        else:
            return render(request, 'public/login.html',
                          {'login_error': "Пара логин/пароль не найдена"})

    return render(request, 'public/login.html')


def user_logout(request):
    """
    Log out user if one is logged in and redirect them to frontpage.
    """

    if request.user.is_authenticated():
        redirect_page = request.POST.get('current_page', '/')
        logout(request)
        # messages.success(request, 'Logged out!')
        return redirect(redirect_page)

    return redirect('frontpage')


def register(request):
    """
    Handles user registration using UserForm from forms.py
    Creates new User and new RedditUser models if appropriate data
    has been supplied.

    If account has been created user is redirected to login page.
    """
    user_form = UserForm()
    if request.user.is_authenticated():
        # messages.warning(request,
        #                 'Вы уже зарегистрированы и вошли')
        return render(request, 'public/register.html', {'form': user_form})

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            print(user_form.cleaned_data["keyWord"])
            if user_form.cleaned_data["keyWord"] == REG_PASSWORD:
                print("complete")
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                reddit_user = ScUser()
                reddit_user.user = user
                reddit_user.save()
                user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
                login(request, user)
                return redirect('frontpage')
            else:
                # messages.error(request,'Неправильный ключ')
                pass

    return render(request, 'public/register.html', {'form': user_form})
