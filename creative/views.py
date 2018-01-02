from django.shortcuts import render

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



def getCreativeByType(request, template, ct, flgPowerCreative):

    if flgPowerCreative:
        tpc = Submission.TP_CHALLENGE
        titleText = 'Боевой Креатив'
    else:
        tpc = Submission.TP_CREATIVE
        titleText = 'Креатив'

    if ct != '':
        all_submissions = Submission.objects.filter(
                                                    tp=tpc,
                                                    creativeType=CreativeType.objects.get(name=ct)
                                                    ).order_by('-score').all()
    else:
        all_submissions = Submission.objects.filter(tp=tpc,
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

def creative(request):
    return getCreativeByType(request,  'creative_lists/creative.html', '',False)


def design(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Дизайн',False)


def conception(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Концепция',False)


def story(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'История',False)


def invention(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Изобретения',False)


def music(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Музыка',False)


def video(request):
    return getCreativeByType(request, 'creative_lists/creative.html', 'Видео',False)

