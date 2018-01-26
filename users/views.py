# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404

from sc.forms import UserForm, ProfileForm
from sc.models import Submission, CreativeType
from sc.views import getCreativeByType
from sc_main.settings.common import REG_PASSWORD, DATE_INPUT_FORMATS
from users.models import ScUser


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = ScUser.objects.get(user=user)

    titleText = 'Портфолио'
    titleLink = '/user/' + username + '/creative/'
    prefix = '/user/' + username + '/creative/'

    return render(request, 'public/profile.html', {
        'profile': profile,
        'flgMainPage': False,
        'canEdit': request.user == user,
        'date': profile.getDate(),
        'power_karma_color': profile.getPowerKarmaColor(),
        'power_karma_val': profile.getShortPowerKarma(),
        'creative_karma_color': profile.getCreativeKarmaColor(),
        'creative_karma_val': profile.getShortCreativeKarma(),
        'titleText': titleText,
        'titleLink': titleLink,
        'prefix' : prefix,
        'ctVal': None,
        'cts': CreativeType.objects.filter(tp=CreativeType.TP_MENU_ITEM),
    })


def user_video(request, username):
    return getCreativeByType(request, 'Видео', Submission.TP_USER_CREATIVE, False, username)


def user_design(request, username):
    return getCreativeByType(request, 'Дизайн', Submission.TP_USER_CREATIVE,False, username)


def user_conception(request, username):
    return getCreativeByType(request, 'Концепция', Submission.TP_USER_CREATIVE, False,username)


def user_story(request, username):
    return getCreativeByType(request, 'Сюжет', Submission.TP_USER_CREATIVE, False,username)


def user_music(request, username):
    return getCreativeByType(request, 'Музыка', Submission.TP_USER_CREATIVE,False, username)


def user_invention(request, username):
    return getCreativeByType(request, 'Изобретения', Submission.TP_USER_CREATIVE, False,username)


def user_creative(request, username):
    return getCreativeByType(request, '', Submission.TP_USER_CREATIVE, False,username)


def new_user_video(request, username):
    return getCreativeByType(request, 'Видео', Submission.TP_USER_CREATIVE,True, username)


def new_user_design(request, username):
    return getCreativeByType(request, 'Дизайн', Submission.TP_USER_CREATIVE,True, username)


def new_user_conception(request, username):
    return getCreativeByType(request, 'Концепция', Submission.TP_USER_CREATIVE,True, username)


def new_user_story(request, username):
    return getCreativeByType(request, 'Сюжет', Submission.TP_USER_CREATIVE,True, username)


def new_user_music(request, username):
    return getCreativeByType(request, 'Музыка', Submission.TP_USER_CREATIVE,True, username)


def new_user_invention(request, username):
    return getCreativeByType(request, 'Изобретения', Submission.TP_USER_CREATIVE,True, username)


def new_user_creative(request, username):
    return getCreativeByType(request, '', Submission.TP_USER_CREATIVE,True, username)

@login_required
def edit_profile(request):
    user = ScUser.objects.get(user=request.user)

    if request.method == 'GET':
        if user.date is None:
            udate = ""
        else:
            udate = user.date.strftime(DATE_INPUT_FORMATS[0])

        profile_form = ProfileForm(instance=user,initial={'date':udate,'about_text':user.about_html})

    elif request.method == 'POST':
        profile_form = ProfileForm(request.POST,request.FILES)
        #print(profile_form)
        if profile_form.is_valid():
            #ScUser.objects.filter(pk=user.pk).update(**profile_form.cleaned_data)
            #print(profile_form.cleaned_data['avatar'])
            user.homepage = profile_form.cleaned_data["homepage"]
            user.about_html = profile_form.cleaned_data["about_text"]
            user.first_name = profile_form.cleaned_data["first_name"]
            user.last_name = profile_form.cleaned_data["last_name"]
            user.email = profile_form.cleaned_data["email"]
            user.date = profile_form.cleaned_data["date"]
            user.tel = profile_form.cleaned_data["tel"]
            user.instagram = profile_form.cleaned_data["instagram"]
            user.fb = profile_form.cleaned_data["fb"]
            user.vk = profile_form.cleaned_data["vk"]
            user.telegram = profile_form.cleaned_data["telegram"]
            user.youtube = profile_form.cleaned_data["youtube"]

            av = profile_form.cleaned_data['avatar']
            if av is not None:
                user.avatar = av
            user.save()
            Z

            #profile.update_profile_data()
            #profile.save()
            messages.success(request, "Настройки профиля сохранены")
    else:
        raise Http404

    return render(request, 'private/edit_profile.html',
                  {'form': profile_form,
                   'caption': 'Добавить пост',
                   'smileLinks': ['img/smiles/smile%d.png'%x for x in range(20)]
                   })


def user_login(request):
    """
    Pretty straighforward user authentication using password and username
    supplied in the POST request.
    """

    if request.user.is_authenticated():
        messages.warning(request, "Вы уже вошли")
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
                messages.error("Доступ запрещён")
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
        messages.success(request, 'Вы вышли')
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
        messages.warning(request,'Вы уже зарегистрированы и вошли')
        return render(request, 'public/register.html', {'form': user_form})

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
          if user_form.cleaned_data["password"]!=user_form.cleaned_data["rep_password"]:
            messages.error(request,'пароли не совпадают')
          else:
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
                messages.warning(request,'Неправильный ключ')
                pass

    return render(request, 'public/register.html', {'form': user_form})
