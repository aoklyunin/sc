from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404

from sc.forms import UserForm, ProfileForm
from sc.models import Submission, Vote, CreativeType
from sc.utils.helpers import post_only
from users.models import ScUser


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = ScUser.objects.get(user=user)

    return render(request, 'public/profile.html', {
        'profile': profile,
        'flgMainPage': False,
        'date': profile.getDate(),
        'portfolio_karma_color': "e9df01",
        'portfolio_karma_val': "12M",
        'creative_karma_color': "a3f001",
        'creative_karma_val': "150",
    })


def getCreativeByType(request, username, template, ct):
    user = ScUser.objects.get(user=User.objects.get(username=username))

    titleText = user.first_name+" "+user.last_name

    if ct != '':
        all_submissions = Submission.objects.filter(author=user,
                                                    tp=Submission.TP_CREATIVE,
                                                    creativeType=CreativeType.objects.get(name=ct)
                                                    ).order_by('-score').all()
    else:
        all_submissions = Submission.objects.filter(author=user,
                                                    tp=Submission.TP_CREATIVE,
                                                    ).order_by('-score').all()
    """
      Serves frontpage and all additional submission listings
      with maximum of 25 submissions per page.
      """
    # TODO: Serve user votes on submissions too.

    paginator = Paginator(all_submissions, 7)

    page = request.GET.get('page', 1)
    try:
        submissions = paginator.page(page)
    except PageNotAnInteger:
        raise Http404
    except EmptyPage:
        submissions = paginator.page(paginator.num_pages)

    submission_votes = {}

    if request.user.is_authenticated():
        for submission in submissions:
            try:
                vote = Vote.objects.get(
                    vote_object_type=submission.get_content_type(),
                    vote_object_id=submission.id,
                    user=ScUser.objects.get(user=request.user))
                submission_votes[submission.id] = vote.value
            except Vote.DoesNotExist:
                pass


    return render(request, template, {
        'submissions': submissions,
        'titleText': titleText,
        'ct':ct,
        'submission_votes': submission_votes
    })


def user_video(request, username):
    return getCreativeByType(request, username, 'public/user_creative_list.html', 'Видео')


def user_design(request, username):
    return getCreativeByType(request, username, 'public/user_creative_list.html', 'Дизайн')


def user_conception(request, username):
    return getCreativeByType(request, username, 'public/user_creative_list.html', 'Концепция')


def user_story(request, username):
    return getCreativeByType(request, username, 'public/user_creative_list.html', 'Сюжет')


def user_music(request, username):
    return getCreativeByType(request, username, 'public/user_creative_list.html', 'Музыка')


def user_invention(request, username):
    return getCreativeByType(request, username, 'public/user_creative_list.html', 'Изобретения')


def user_creative(request, username):
    return getCreativeByType(request, username, 'public/user_creative_list.html', '')


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
            messages.success(request, "Profile settings saved")
    else:
        raise Http404

    return render(request, 'private/edit_profile.html', {'form': profile_form})


def user_login(request):
    """
    Pretty straighforward user authentication using password and username
    supplied in the POST request.
    """

    if request.user.is_authenticated():
        messages.warning(request, "You are already logged in.")
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


@post_only
def user_logout(request):
    """
    Log out user if one is logged in and redirect them to frontpage.
    """

    if request.user.is_authenticated():
        redirect_page = request.POST.get('current_page', '/')
        logout(request)
        messages.success(request, 'Logged out!')
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
        messages.warning(request,
                         'You are already registered and logged in.')
        return render(request, 'public/register.html', {'form': user_form})

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
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

    return render(request, 'public/register.html', {'form': user_form})
